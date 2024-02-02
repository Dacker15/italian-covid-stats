FROM python:3.9-bookworm

RUN pip install requests
RUN pip install python-logstash-async
RUN pip install arrow
RUN pip install python-dotenv

COPY python/fetch/ /
COPY utils/wait-for-it.sh /

CMD [ "./wait-for-it.sh", "logstash:3001", "--strict", "--", "python", "./server.py" ]