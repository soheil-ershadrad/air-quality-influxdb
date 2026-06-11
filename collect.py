import os
import requests
from influxdb_client_3 import InfluxDBClient3, Point

# ----------------------------------------------------------
# InfluxDB configuration 
# ----------------------------------------------------------

INFLUX_HOST = os.environ["INFLUX_HOST"]
INFLUX_TOKEN = os.environ["INFLUX_TOKEN"]
INFLUX_DATABASE = os.environ["INFLUX_DATABASE"]

# ----------------------------------------------------------
# Stockholm coordinates
# ----------------------------------------------------------

LATITUDE = 59.3293
LONGITUDE = 18.0686

# ----------------------------------------------------------
# Air quality API
# ----------------------------------------------------------

url = (
    "https://air-quality-api.open-meteo.com/v1/air-quality"
    f"?latitude={LATITUDE}"
    f"&longitude={LONGITUDE}"
    "&current=pm10,pm2_5,nitrogen_dioxide,ozone"
)

response = requests.get(url, timeout=30)
response.raise_for_status()

data = response.json()

current = data["current"]

pm25 = float(current["pm2_5"])
pm10 = float(current["pm10"])
no2 = float(current["nitrogen_dioxide"])
o3 = float(current["ozone"])

# ----------------------------------------------------------
# Connect to InfluxDB
# ----------------------------------------------------------

client = InfluxDBClient3(
    host=INFLUX_HOST,
    token=INFLUX_TOKEN,
    database=INFLUX_DATABASE,
)

# ----------------------------------------------------------
# Create point
# ----------------------------------------------------------

point = (
    Point("air_quality")
    .tag("city", "Stockholm")
    .tag("country", "Sweden")
    .field("pm25", pm25)
    .field("pm10", pm10)
    .field("no2", no2)
    .field("o3", o3)
)

# ----------------------------------------------------------
# Write point
# ----------------------------------------------------------

client.write(record=point)

print("Successfully wrote point")
print(
    {
        "city": "Stockholm",
        "pm25": pm25,
        "pm10": pm10,
        "no2": no2,
        "o3": o3,
    }
)
