FROM ubuntu:jammy

ENV SPARK_HOME "/opt/spark"
ENV PATH ${SPARK_HOME}/bin:$PATH
ENV PATH ${SPARK_HOME}/sbin:$PATH

ARG SPARK_VERSION="3.5.0"
ARG HADOOP_VERSION="3"

RUN apt update
RUN apt install -y procps gcc wget tar make default-jre default-jdk build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev curl

# Install Python 3.9.18

RUN wget https://www.python.org/ftp/python/3.9.18/Python-3.9.18.tar.xz -P /opt
RUN tar -xf /opt/Python-3.9.18.tar.xz -C /opt
WORKDIR /opt/Python-3.9.18
RUN ./configure
RUN make install
RUN pip3 install elasticsearch kafka-python numpy pyspark pyarrow pandas python-dotenv

# Install Spark

RUN wget https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -P /opt

RUN tar -xvzf /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -C /opt

RUN mv /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} ${SPARK_HOME}

HEALTHCHECK --interval=10s --timeout=10s --retries=20 CMD [ "curl", "-f", "http://localhost:4040" ]

COPY spark/trainer /opt/trainer

CMD [ "spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.elasticsearch:elasticsearch-spark-30_2.12:8.12.0", "/opt/trainer/main.py" ]