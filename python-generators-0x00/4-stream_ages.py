import psycopg2
from psycopg2.extras import RealDictCursor

def stream_user_ages():
    """
    Generator that connects to DB and yields user ages one by one from user_data table.
    Uses a server-side cursor for memory efficiency and only one loop.
    """
    conn = psycopg2.connect(
        dbname="your_db_name",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    )
    try:
        with conn.cursor(name="age_cursor", cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT age FROM user_data;")
            for row in cursor:
                yield row['age']
    finally:
        conn.close()

def calculate_average_age():
    """
    Uses stream_user_ages generator to compute average age without loading all data in memory.
    Uses only one additional loop.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        if age is not None:  # skip NULL values if any
            total_age += age
            count += 1

    average_age = total_age / count if count > 0 else 0
    print(f"Average age of users: {average_age}")

if __name__ == "__main__":
    calculate_average_age()
