FROM docker.elastic.co/elasticsearch/elasticsearch:8.12.0

ENV cluster.routing.allocation.disk.threshold_enabled=false
ENV cluster.name=elasticsearch
ENV discovery.type=single-node
ENV xpack.security.enabled=false
ENV bootstrap.memory_lock=true
ENV logger.level=WARN
ENV ES_JAVA_OPTS="-Xms1g -Xmx4g"

EXPOSE 9200

HEALTHCHECK --interval=10s --timeout=10s --retries=20 CMD [ "curl", "-f", "http://localhost:9200" ]