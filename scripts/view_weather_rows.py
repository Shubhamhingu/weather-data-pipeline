import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from utils.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

# Using SQLAlchemy (removes warning)
engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Query first 10 rows
query = "SELECT * FROM weather ORDER BY recorded_at DESC LIMIT 10;"
df = pd.read_sql(query, engine)

print(" First 10 rows:")
print(df.head(10))
