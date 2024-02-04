from functions import *
from dotenv import load_dotenv


def start():
    load_dotenv()
    print("Starting the Spark Application")
    context, instance = get_spark_instance()
    elastic_instance = get_elastic_index()
    kafka_input_df = get_kafka_instance(instance)
    print("Spark started. Kafka input ready.")
    kafka_input_df.writeStream.foreachBatch(process_batch).start().awaitTermination()
    instance.stop()


start()
