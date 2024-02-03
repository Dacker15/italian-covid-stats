from functions import *
from dotenv import load_dotenv


def start():
    load_dotenv()
    print("Starting the Spark Application")
    context, instance = get_spark_instance()
    elastic_instance = get_elastic_index()
    kafka_input = get_kafka_instance(instance)
    print("Spark started. Kafka input ready.")
    raw_data_to_dataframe(kafka_input)


start()
