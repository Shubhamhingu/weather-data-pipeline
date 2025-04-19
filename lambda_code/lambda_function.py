from weather_etl import extract, transform, load
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


def lambda_handler(event, context):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    db_config = {
        "host": os.getenv("DB_HOST"),
        "port": "5432",
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASS"),
        "dbname": os.getenv("DB_NAME")
    }

    data = extract(api_key, "/tmp/major_cities.json")  # or include it in your zip
    df = transform(data)
    load(df, db_config)

    return {"statusCode": 200, "body": "ETL completed successfully."}
