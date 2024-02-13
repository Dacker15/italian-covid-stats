# Italian Covid Stats

This pipeline is used to extract the Italian Covid-19 stats from the official Italian Civil Protection website in order to analyze it and predict the future trend of the virus.

## Setup

All process is Dockerized, so you need to have Docker installed on your machine.  
After it, you can run the following command to build the image and run the pipeline:

```bash
docker compose up
```

## Load Kibana Dashboard

To load created Kibana Dashboard, you have to run the following command:

```bash
cd kibana_loader
./entrypoint.sh dashboard.ndjson
```
