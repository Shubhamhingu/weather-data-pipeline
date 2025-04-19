import psycopg2
from utils.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)
cur = conn.cursor()

cur.execute("""
    DROP TABLE IF EXISTS weather;

    CREATE TABLE weather (
        latitude DOUBLE PRECISION,
        longitude DOUBLE PRECISION,
        country TEXT,
        timezone_offset_sec INT,
        sunrise TIMESTAMP,
        sunset TIMESTAMP,
        weather_main TEXT,
        weather_description TEXT,
        temperature_celsius DOUBLE PRECISION,
        temperature_fahrenheit DOUBLE PRECISION,
        temperature_min_celsius DOUBLE PRECISION,
        temperature_max_celsius DOUBLE PRECISION,
        feels_like_celsius DOUBLE PRECISION,
        pressure_hPa INT,
        sea_level_hPa INT,
        visibility_meters INT,
        wind_speed_kph DOUBLE PRECISION,
        wind_direction_deg INT,
        cloud_coverage_percent INT,
        location_name TEXT,
        recorded_at TIMESTAMP
    );
""")

conn.commit()
cur.close()
conn.close()

print("✅ Weather table has been successfully reset.")
