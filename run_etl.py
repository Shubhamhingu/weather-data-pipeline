# run_etl.py
from lambda_code.weather_etl import extract, transform, load
from utils.config import (
    OPENWEATHER_API_KEY,
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASS
)

if __name__ == "__main__":
    print(" Starting ETL script...")

    # 1. Extract
    data = extract(api_key=OPENWEATHER_API_KEY, json_path="lambda_code/major_cities.json")
    print(f" Extracted {len(data)} records")

    # 2. Transform
    df = transform(data)
    print(f" Transformed data into DataFrame with {len(df)} rows")

    # 3. Load
    db_config = {
        "host": DB_HOST,
        "port": DB_PORT,
        "dbname": DB_NAME,
        "user": DB_USER,
        "password": DB_PASS
    }
    load(df, db_config)
    print(" Loaded data into PostgreSQL")

    print(" ETL process completed.")
