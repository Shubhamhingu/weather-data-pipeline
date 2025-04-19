import requests
import pandas as pd
from sqlalchemy import create_engine
import json
from datetime import datetime
import logging
import os

try:
    from utils.config import (
        OPENWEATHER_API_KEY,
        DB_HOST,
        DB_PORT,
        DB_NAME,
        DB_USER,
        DB_PASS,
        S3_BUCKET
    )
except ImportError:
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    S3_BUCKET = os.getenv("S3_BUCKET")


# Set up logging (for local testing or CloudWatch via print in Lambda)
logging.basicConfig(
    filename="weather_data.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def kelvin_to_celsius(k):
    return round(k - 273.15, 2)

def kelvin_to_fahrenheit(k):
    return round((k - 273.15) * 9/5 + 32, 2)

def unix_to_datetime(unix_time, timezone_offset_sec=0):
    return datetime.utcfromtimestamp(unix_time + timezone_offset_sec).strftime('%Y-%m-%d %H:%M:%S')

# --------------------
# EXTRACT
# --------------------
def extract(api_key, json_path="major_cities.json"):
    with open(json_path, 'r', encoding='utf-8') as cities_file:
        cities_data = json.load(cities_file)

    major_cities = [city for city in cities_data if city['country'] in ['IN', 'US']]
    
    ids = []
    tempStr = ""
    cnt = 0
    for city in major_cities:
        if cnt == 19:
            tempStr += str(city['id'])
            ids.append(tempStr)
            tempStr = ""
            cnt = 0
        else:
            tempStr += str(city['id']) + ','
            cnt += 1
    if tempStr:
        ids.append(tempStr.rstrip(','))  # Catch any leftover

    all_data = []
    for id_group in ids:
        url = f"https://api.openweathermap.org/data/2.5/group?id={id_group}&appid={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            all_data.extend(json_data["list"])
        else:
            logging.error(f"Failed for ID group: {id_group} - Status code: {response.status_code}")
    return all_data

# --------------------
# TRANSFORM
# --------------------
def transform(data):
    transformed_list = []
    recorded_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for record in data:
        parsed = {
            "latitude": record["coord"]["lat"],
            "longitude": record["coord"]["lon"],
            "country": record["sys"]["country"],
            "timezone_offset_sec": record.get("timezone", 0),  
            "sunrise": unix_to_datetime(record["sys"]["sunrise"], record.get("timezone", 0)),  # ✅ Fixed
            "sunset": unix_to_datetime(record["sys"]["sunset"], record.get("timezone", 0)),    # ✅ Fixed
            "weather_main": record["weather"][0]["main"],
            "weather_description": record["weather"][0]["description"],
            "temperature_celsius": kelvin_to_celsius(record["main"]["temp"]),
            "temperature_fahrenheit": kelvin_to_fahrenheit(record["main"]["temp"]),
            "temperature_min_celsius": kelvin_to_celsius(record["main"]["temp_min"]),
            "temperature_max_celsius": kelvin_to_celsius(record["main"]["temp_max"]),
            "feels_like_celsius": kelvin_to_celsius(record["main"]["feels_like"]),
            "visibility_meters": record.get("visibility", None),
            "wind_speed_kph": round(record["wind"]["speed"] * 3.6, 2),
            "wind_direction_deg": record["wind"].get("deg", None),
            "cloud_coverage_percent": record["clouds"]["all"],
            "location_name": record["name"],
            "recorded_at": recorded_time
        }
        transformed_list.append(parsed)

    return pd.DataFrame(transformed_list)

# --------------------
# LOAD
# --------------------
def load(df, db_config):
    logging.info("Loading data to PostgreSQL...")
    try:
        engine = create_engine(
            f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
        )
        df.to_sql("weather", engine, if_exists="append", index=False)
        logging.info(" Data loaded successfully.")
    except Exception as e:
        logging.error(" Failed to load data: " + str(e))
        raise e
