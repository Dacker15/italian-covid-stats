import os
import pandas as pd

from pyspark import SparkContext
from elasticsearch import Elasticsearch
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.session import SparkSession

from mapping import ELASTICSEARCH_BODY

app_name = "ItalianCovidStats"


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
    kafka_instance = f"{kafka_host}:{kafka_port}"
    return (
        spark_instance.readStream.format("kafka")
        .option("kafka.bootstrap.servers", kafka_instance)
        .option("subscribe", kafka_topic)
        .load()
    )


def raw_data_to_dataframe(raw_data: DataFrame):
    raw_df = raw_data.select("message")
    print("Raw Dataframe", raw_df, raw_df.head(5))
