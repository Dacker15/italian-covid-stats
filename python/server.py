import arrow
import logstash_async
import requests

start_date = arrow.Arrow(year=2020, month=2, day=24)
test_date = arrow.utcnow().shift(weeks=-1)
end_date = (
    arrow.utcnow().shift(weekday=4, weeks=-1)
    if arrow.utcnow().weekday() >= 4
    else arrow.utcnow().shift(weeks=-2, weekday=4)
)

actual_date = test_date

while actual_date <= end_date:
    year = actual_date.date().year
    month = str(actual_date.date().month).rjust(2, "0")
    day = str(actual_date.date().day).rjust(2, "0")
    url = f"https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-{year}{month}{day}.csv"

    response = requests.get(url)
    print("Response for", year, month, day, response.text, "\n")

    actual_date = actual_date.shift(days=1)
