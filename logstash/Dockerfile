FROM docker.elastic.co/logstash/logstash-oss:8.11.2

RUN rm -rf /usr/share/logstash/pipeline

COPY logstash/pipeline/logstash.conf /usr/share/logstash/pipeline/logstash.conf

ENV PIPELINE_WORKERS=1
ENV TCP_PORT=3001

EXPOSE 3001