import psycopg2
from psycopg2.extras import RealDictCursor

def paginate_users(page_size, offset):
    """
    Fetch a page of users from user_data table with limit and offset.
    Returns a list of user rows (dict).
    """
    conn = psycopg2.connect(
        dbname="your_db_name",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    )
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM user_data ORDER BY user_id LIMIT %s OFFSET %s",
                (page_size, offset)
            )
            return cursor.fetchall()
    finally:
        conn.close()


def lazypaginate(page_size):
    """
    Generator that fetches rows page by page from user_data table,
    yielding one user at a time.
    Uses a single loop to fetch next page lazily only when needed.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        for user in page:
            yield user
        offset += page_size
