from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta

import requests

app = Flask(__name__)
CORS(app)


@app.route("/fetch", methods=["GET"])
def fetch_data():
    responses = get_data()
    return jsonify({"message": responses})


def get_data():
    responses = list()
    end_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    print(
        f"Fetch request from {end_date.year}-{str(end_date.month).rjust(2, '0')}-{str(end_date.day).rjust(2, '0')}"
    )
    start_date = end_date - timedelta(weeks=1)
    while start_date.timestamp() < end_date.timestamp():
        year = start_date.year
        month = str(start_date.month).rjust(2, "0")
        day = str(start_date.day).rjust(2, "0")
        url = f"https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-{year}{month}{day}.csv"

        response = requests.get(url)

        if response.status_code == 200:
            responses.append(response.text)
        else:
            print("Error for", year, month, day, "Skipping", "\n")

        start_date += timedelta(days=1)

    return responses


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
