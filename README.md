# Italian Covid Stats

This pipeline is used to extract the Italian Covid-19 stats from the official Italian Civil Protection website in order to analyze it and predict the future trend of the virus.

## Structure
You can run this project in two modes:
- Simulation: data will load from beginning of dataset to end.
- Production: data will load every Saturday at midnight.

You can choose the mode by comment / uncomment Logstash and Python Server images in `docker-compose.yml`.  
Make sure you select all production / non-production images.


## Setup

All process is Dockerized, so you need to have Docker installed on your machine.  
After it, you can run the following command to build the images and run the pipeline:

```bash
docker compose up
```

Now, you have to load Kibana Dashboard, using the following command:
```bash
cd kibana_loader
./entrypoint.sh dashboard.ndjson
```

Then, just simply open Kibana and wait for data to appear
