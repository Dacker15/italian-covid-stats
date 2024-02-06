import io
import json
import os
import pandas as pd

from dateutil.parser import parse
from pyspark import SparkContext
from elasticsearch import Elasticsearch
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegressionModel, LinearRegression
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.session import SparkSession

from mapping import ELASTICSEARCH_BODY, SPARK_DATA_MAPPING

app_name = "ItalianCovidStats"
key_map = {
    "hospitalized": "ricoverati_con_sintomi",
    "intensive_care": "terapia_intensiva",
    "home_isolation": "isolamento_domiciliare",
}


def get_spark_instance():
    sc = SparkContext(master="local[*]", appName=app_name)
    sc.setLogLevel("ERROR")

    spark = SparkSession(sc).builder.appName(app_name).getOrCreate()
    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

    return sc, spark


def get_elastic_index():
    elastic_host = os.getenv("ELASTICSEARCH_HOST")
    elastic_port = int(os.getenv("ELASTICSEARCH_PORT"))
    elastic_complete = f"http://{elastic_host}:{elastic_port}"
    elastic_index = os.getenv("ELASTICSEARCH_INDEX")
    elastic_connection = Elasticsearch(hosts=elastic_complete)
    response = elastic_connection.indices.create(
        index=elastic_index, body=ELASTICSEARCH_BODY, ignore=400
    )

    if response["acknowledged"]:
        print("Successful index creation with response", response["index"])

    return elastic_connection


def get_kafka_instance(spark_instance: SparkSession):
    kafka_host = os.getenv("KAFKA_HOST")
    kafka_port = os.getenv("KAFKA_PORT")
    kafka_topic = os.getenv("KAFKA_TOPIC")
    kafka_instance = f"http://{kafka_host}:{kafka_port}"
    return (
        spark_instance.readStream.format("kafka")
        .option("kafka.bootstrap.servers", kafka_instance)
        .option("subscribe", kafka_topic)
        .load()
    )


def get_prev_data(elastic_instance: Elasticsearch, region_code: str, timestamp: int):
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"region": region_code}},
                    {"range": {"timestamp": {"lt": timestamp}}},
                ]
            }
        }
    }
    response = elastic_instance.search(
        index=os.getenv("ELASTICSEARCH_INDEX"), body=query
    )
    return [hit["_source"] for hit in response["hits"]["hits"]]


def process_batch(
    raw_data: DataFrame,
    data_batch_id: int,
    spark_instance: SparkSession,
    elastic_instance: Elasticsearch,
):
    print("Processing batch", data_batch_id)

    if raw_data.isEmpty():
        print("No data to process")
        return

    raw_row = raw_data.first()
    raw_value: bytearray = raw_row["value"]
    decoded_value = raw_value.decode("utf-8")
    json_value = json.loads(decoded_value)
    csv_raw_value = io.StringIO(json_value["message"])
    csv_value = pd.read_csv(csv_raw_value, sep=",")

    # Create empty output data frame
    output_df = spark_instance.createDataFrame([], SPARK_DATA_MAPPING)

    for _, row in csv_value.iterrows():
        # Get day date and convert it to timestamp
        date = row["data"]
        parsed_date = parse(date)
        parsed_date = parsed_date.replace(hour=0, minute=0, second=0, microsecond=0)
        formatted_date = f"{parsed_date.year}-{str(parsed_date.month).ljust(2, '0')}-{str(parsed_date.day).ljust(2, '0')}"
        timestamp = int(parsed_date.timestamp())

        # Get region code
        region_code = row["codice_regione"]

        # Get previous data
        prev_data = get_prev_data(elastic_instance, region_code, timestamp)
        print("Previous data", prev_data)

        for regressor_type in key_map.keys():
            # Get dependent variable for regression
            y_value = row[key_map[regressor_type]]

            # TODO: Regression: use prev data only and use it to predict today value

            # Define regression data frame
            regression_data = [
                (prev["timestamp"], prev[regressor_type]) for prev in prev_data
            ]
            regression_data.append((timestamp, y_value))
            regression_df = spark_instance.createDataFrame(
                regression_data, ["timestamp", "sick"]
            )

            # Train regressor
            assembler = VectorAssembler(inputCols=["timestamp"], outputCol="features")
            regression_df = assembler.transform(regression_df)
            lr = LinearRegression(featuresCol="features", labelCol="sick")
            model: LinearRegressionModel = lr.fit(regression_df)

            test_df = spark_instance.createDataFrame(
                [(timestamp, y_value)], ["timestamp", "sick"]
            )
            test_df = assembler.transform(test_df)
            prediction: float = model.transform(test_df).collect()[0]["prediction"]
            print(f"Prediction for {regressor_type} is {prediction} and {y_value}")

        # Create region output data frame
        region_output_df = spark_instance.createDataFrame(
            [
                (
                    formatted_date,
                    timestamp,
                    region_code,
                    row["isolamento_domiciliare"],
                    row["ricoverati_con_sintomi"],
                    row["terapia_intensiva"],
                )
            ],
            SPARK_DATA_MAPPING,
        )

        # Append region output data frame to the global output data frame
        output_df = output_df.union(region_output_df)

    # Write to ElasticSearch
    output_df.write.format("org.elasticsearch.spark.sql").option(
        "es.resource", os.getenv("ELASTICSEARCH_INDEX")
    ).option("es.nodes", os.getenv("ELASTICSEARCH_HOST")).option(
        "es.port", os.getenv("ELASTICSEARCH_PORT")
    ).mode(
        "append"
    ).save()
