import io
import json
import os
import pandas as pd

from pyspark import SparkContext
from elasticsearch import Elasticsearch
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegressionModel, LinearRegression
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.session import SparkSession

from mapping import ELASTICSEARCH_BODY

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


def get_regressor(region_code: str, regressor_type: str):
    try:
        return LinearRegressionModel.load(
            f"{os.getenv('MODEL_PATH')}/{region_code}_{regressor_type}"
        )
    except:
        print("No model found for", region_code, regressor_type, "Creating a new one")
        return LinearRegressionModel()


def store_regressor(
    regressor: LinearRegressionModel, region_code: str, regressor_type: str
):
    regressor.write().overwrite().save(
        f"{os.getenv('MODEL_PATH')}/{region_code}_{regressor_type}"
    )


def train_single_regressor(
    data_frame: pd.DataFrame, regressor_type: str, instance: SparkSession
) -> LinearRegressionModel:
    spark_df = instance.createDataFrame(data_frame)
    map_x = VectorAssembler(inputCols=[key_map[regressor_type]], outputCol="features")
    train_df = map_x.transform(spark_df)
    regression = LinearRegression(
        featuresCol="features",
        labelCol=f"{key_map[regressor_type]}_predicted",
        maxIter=10,
        regParam=0.3,
    )

    return regression.fit(train_df)


def evaluate_regressor(
    data_frame: pd.DataFrame,
    regressor: LinearRegressionModel,
    regressor_type: str,
    instance: SparkSession,
) -> LinearRegressionModel:
    spark_df = instance.createDataFrame(data_frame)
    map_x = VectorAssembler(inputCols=[key_map[regressor_type]], outputCol="features")
    train_df = map_x.transform(spark_df)
    prediction = regressor.transform(train_df)
    prediction.show()
    prediction = prediction.toPandas()
    print(prediction)
    print("Predicted value for", regressor_type, "is", prediction)


def process_batch(
    raw_data: DataFrame, data_batch_id: int, spark_instance: SparkSession
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

    for _, row in csv_value.iterrows():
        for regressor_type in key_map.keys():
            regressor = get_regressor(row["codice_regione"], regressor_type)
            # Next line is commented out because it's not working
            # next_regressor = train_single_regressor(row, regressor_type, spark_instance)
            # store_regressor(next_regressor, row["codice_regione"], regressor_type)

            # evaluate_regressor(row, next_regressor, regressor_type, spark_instance)
