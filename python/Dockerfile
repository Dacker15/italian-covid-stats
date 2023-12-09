FROM python:3.9-alpine

RUN pip install requests
RUN pip install python-logstash-async
RUN pip install arrow
RUN pip install python-dotenv

COPY python/fetch/ /

CMD ["python", "./server.py"]