# 0-stream_users.py

import psycopg2
from psycopg2.extras import RealDictCursor

def stream_users():

    # Adjust connection parameters as needed
    conn = psycopg2.connect(
        dbname="your_db_name",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    )

    try:
        with conn.cursor(name="user_cursor", cursor_factory=RealDictCursor) as cursor:
            # Server-side cursor fetches rows lazily without loading all data into memory
            cursor.execute("SELECT * FROM user_data;")

            for row in cursor:
                yield row

    finally:
        conn.close()
