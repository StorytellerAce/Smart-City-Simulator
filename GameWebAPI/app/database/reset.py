from pathlib import Path
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="teoh0628",
    port=5432
)

cursor = conn.cursor()

schema = Path("GameWebAPI/app/database/schema.sql").read_text()

cursor.execute(schema)

conn.commit()

cursor.close()
conn.close()

print("Database recreated successfully.")