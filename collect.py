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

air_url = (
    "https://air-quality-api.open-meteo.com/v1/air-quality"
    f"?latitude={LATITUDE}"
    f"&longitude={LONGITUDE}"
    "&current=pm10,pm2_5,nitrogen_dioxide,ozone"
)

air_response = requests.get(air_url, timeout=30)
air_response.raise_for_status()

air_data = air_response.json()["current"]

# ----------------------------------------------------------
# Weather API
# ----------------------------------------------------------

weather_url = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={LATITUDE}"
    f"&longitude={LONGITUDE}"
    "&current=temperature_2m,"
    "relative_humidity_2m,"
    "wind_speed_10m"
)

weather_response = requests.get(weather_url, timeout=30)
weather_response.raise_for_status()

weather_data = weather_response.json()["current"]

# ----------------------------------------------------------
# Extract variables
# ----------------------------------------------------------

pm25 = float(air_data["pm2_5"])
pm10 = float(air_data["pm10"])
no2 = float(air_data["nitrogen_dioxide"])
o3 = float(air_data["ozone"])

temperature = float(weather_data["temperature_2m"])
humidity = float(weather_data["relative_humidity_2m"])
wind_speed = float(weather_data["wind_speed_10m"])

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
    .field("pm25", pm25)
    .field("pm10", pm10)
    .field("no2", no2)
    .field("o3", o3)
    .field("temperature", temperature)
    .field("humidity", humidity)
    .field("wind_speed", wind_speed)
)

# ----------------------------------------------------------
# Write point
# ----------------------------------------------------------

client.write(record=point)

print("Successfully wrote point")
print(
    {
        "pm25": pm25,
        "pm10": pm10,
        "no2": no2,
        "o3": o3,
        "temperature": temperature,
        "humidity": humidity,
        "wind_speed": wind_speed,
    }
)
