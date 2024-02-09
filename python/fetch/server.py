import arrow
import dotenv
import logstash_async.handler
import logging
import os
import requests
import time

from datetime import datetime, timedelta

dotenv.load_dotenv()

time.sleep(float(os.getenv("WARMUP_SECONDS")))

logger = logging.getLogger("python-logstash-logger")
logger.setLevel(logging.INFO)

host = os.getenv("LOGSTASH_HOST")
port = os.getenv("LOGSTASH_PORT")
handler = logstash_async.handler.AsynchronousLogstashHandler(
    host, int(port), database_path=""
)
logger.addHandler(handler)

start_date = datetime(year=2020, month=2, day=24)
test_date = datetime.utcnow() - timedelta(weeks=4)

current_date = datetime.utcnow()
if current_date.weekday() >= 4:
    end_date = current_date + timedelta(weeks=-1, days=current_date.weekday() - 4)
else:
    end_date = current_date + timedelta(weeks=-2, days=current_date.weekday() + 3)


actual_date = test_date

while actual_date <= end_date:
    year = actual_date.year
    month = str(actual_date.month).rjust(2, "0")
    day = str(actual_date.day).rjust(2, "0")
    url = f"https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-{year}{month}{day}.csv"

    response = requests.get(url)

    if response.status_code == 200:
        logger.info(response.text)
    else:
        print("Error for", year, month, day, "Skipping", "\n")

    actual_date += timedelta(days=1)

    time.sleep(float(os.getenv("SLEEP_SECONDS")))
