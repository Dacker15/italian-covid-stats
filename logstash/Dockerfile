FROM docker.elastic.co/logstash/logstash-oss:8.11.2

RUN rm -rf /usr/share/logstash/config
RUN rm -rf /usr/share/logstash/pipeline

COPY logstash/pipeline/ /usr/share/logstash/pipeline/
COPY logstash/config/ /usr/share/logstash/config/

ENV TCP_PORT=3001

EXPOSE 3001