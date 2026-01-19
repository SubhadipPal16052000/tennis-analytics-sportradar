import psycopg
from db_config import DB_CONNECT_ARGS
import os

print("DB_HOST =", os.getenv("DB_HOST"))

conn = psycopg.connect(**DB_CONFIG)
cur = conn.cursor()
cur.execute("SELECT inet_server_addr();")
print("Server IP:", cur.fetchone()[0])

cur.close()
conn.close()

print("✅ Database connection successful")
