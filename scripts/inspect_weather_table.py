import psycopg2
from utils.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

query = """
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'weather'
ORDER BY ordinal_position;
"""

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cur = conn.cursor()
    cur.execute(query)
    columns = cur.fetchall()

    print("📋 Columns in 'weather' table:")
    for col in columns:
        print(f"- {col[0]} ({col[1]})")

    cur.close()
    conn.close()

except Exception as e:
    print("❌ Failed to inspect table:", e)
