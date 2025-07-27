import psycopg2
from psycopg2.extras import RealDictCursor

def stream_users_in_batches(batch_size):
   
    conn = psycopg2.connect(
        dbname="your_db_name",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    )
    try:
        with conn.cursor(name="user_batch_cursor", cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM user_data;")
            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch
    finally:
        conn.close()

def batch_processing(batch_size):
    """
    Processes batches of users fetched from stream_users_in_batches.
    Filters each batch to only yield users over the age of 25.
    Uses yield generator to yield users one by one.
    """
    for batch in stream_users_in_batches(batch_size):
        # Loop over each user in batch and yield if over 25
        for user in batch:
            if user.get('age', 0) > 25:
                yield user
