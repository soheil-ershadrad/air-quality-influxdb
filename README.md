# Air Quality Monitoring and Forecasting with InfluxDB 3

## Overview

This project collects real-time air quality and weather data for Stockholm, Sweden, and stores the measurements in InfluxDB 3 Cloud Serverless. Data ingestion is automated using GitHub Actions and runs every 5 minutes without requiring dedicated infrastructure.

The long-term goal is to build machine learning models for air quality forecasting.

## Architecture

```text
Open-Meteo APIs
        ↓
GitHub Actions
        ↓
InfluxDB 3 Cloud Serverless
        ↓
Machine Learning Models
```

## Features

* Automated data collection every 5 minutes
* Cloud-hosted time-series database using InfluxDB 3
* Serverless architecture with no dedicated VM required
* Real-time air quality monitoring
* Weather-enhanced dataset for forecasting applications
* GitHub Actions based scheduling and deployment

## Data Sources

### Air Quality

Data is retrieved from the Open-Meteo Air Quality API.

Collected variables:

* PM2.5
* PM10
* Nitrogen Dioxide (NO₂)
* Ozone (O₃)

### Weather

Data is retrieved from the Open-Meteo Weather API.

Collected variables:

* Temperature
* Relative Humidity
* Wind Speed

## Database Schema

Measurement:

```text
air_quality
```

Tags:

```text
city
```

Fields:

```text
pm25
pm10
no2
o3
temperature
humidity
wind_speed
```

## Technology Stack

* Python
* InfluxDB 3 Cloud Serverless
* GitHub Actions
* Open-Meteo APIs
* Pandas
* Jupyter Notebooks

## Repository Structure

```text
.
├── collect.py
├── requirements.txt
├── README.md
└── .github
    └── workflows
        └── collect.yml
```

## Automation

Data collection is executed automatically through GitHub Actions using a cron schedule.

```yaml
schedule:
  - cron: '*/5 * * * *'
```
