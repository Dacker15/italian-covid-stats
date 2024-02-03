docker stop italian-covid-stats-kafka-topic-1 
docker stop italian-covid-stats-kafka-server-1 
docker stop italian-covid-stats-kafka-ui-1
docker stop italian-covid-stats-python_server-1 
docker stop italian-covid-stats-logstash-1 
docker stop italian-covid-stats-spark-1
docker stop italian-covid-stats-elasticsearch-1
docker rm italian-covid-stats-kafka-topic-1 
docker rm italian-covid-stats-kafka-server-1 
docker rm italian-covid-stats-kafka-ui-1
docker rm italian-covid-stats-python_server-1 
docker rm italian-covid-stats-logstash-1 
docker rm italian-covid-stats-spark-1
docker rm italian-covid-stats-elasticsearch-1
docker image rm italian-covid-stats-kafka-server:latest 
docker image rm italian-covid-stats-kafka-ui:latest 
docker image rm italian-covid-stats-kafka-topic:latest 
docker image rm italian-covid-stats-logstash:latest 
docker image rm italian-covid-stats-python_server:latest
docker image rm italian-covid-stats-spark:latest
docker image rm italian-covid-stats-elasticsearch:latest