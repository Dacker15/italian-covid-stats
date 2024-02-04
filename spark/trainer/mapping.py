ELASTICSEARCH_BODY = {
    "mappings": {
        "properties": {
            "date": {"type": "date", "format": "yyyy-MM-dd"},
            "region": {"type": "keyword"},
            "home_isolation": {"type": "integer"},
            "hospitalized": {"type": "integer"},
            "intensive_care": {"type": "integer"},
        },
    },
}
