# create a decorator that retries database operations if they fail due to transient errors
import sqlite3
from sqlite3 import Error
import functools
import time


def retry_on_failure(func, retries=3, delays=2):
    pass

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            connection = sqlite3.connect('users.db')
            value = func(connection, *args, **kwargs)
            connection.close()
            return value
        except Error as e:
            return e
    return wrapper

@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)