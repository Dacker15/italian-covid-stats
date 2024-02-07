from pyspark.sql import types as tp


ELASTICSEARCH_BODY = {
    "mappings": {
        "properties": {
            "date": {"type": "date", "format": "yyyy-MM-dd"},
            "timestamp": {"type": "integer"},
            "region": {"type": "keyword"},
            "home_isolation": {"type": "integer"},
            "hospitalized": {"type": "integer"},
            "intensive_care": {"type": "integer"},
        },
    },
}


SPARK_DATA_MAPPING = tp.StructType(
    [
        tp.StructField("date", tp.StringType(), nullable=False),
        tp.StructField("timestamp", tp.IntegerType(), nullable=False),
        tp.StructField("region", tp.StringType(), nullable=False),
        tp.StructField("home_isolation", tp.IntegerType(), nullable=False),
        tp.StructField("hospitalized", tp.IntegerType(), nullable=False),
        tp.StructField("intensive_care", tp.IntegerType(), nullable=False),
        tp.StructField("predicted_home_isolation", tp.IntegerType(), nullable=True),
        tp.StructField("predicted_hospitalized", tp.IntegerType(), nullable=True),
        tp.StructField("predicted_intensive_care", tp.IntegerType(), nullable=True),
    ]
)
