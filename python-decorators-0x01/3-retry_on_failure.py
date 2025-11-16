# create a decorator that retries database operations if they fail due to transient errors
import sqlite3
from sqlite3 import Error
import functools
import time

# When dealing with decorators that take arguments, you have three levels:
# Level 1 - Takes in the arguments of the decorator
# Level 2 - Takes in the func to decorate
# Level 3 - Takes the args of the func and executes it
def retry_on_failure(retries=3, delays=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    value = func(*args, **kwargs)
                    return value # If func is successful, we return the value and it exits the loop completely
                except Error as e:
                    print(f"Error occured: {e}.Attempt {attempt + 1}/{retries}")
                    if attempt < retries - 1:
                        time.sleep(delays)
                    else:
                        print("All retries depleted")
                        raise # Re-raise the exception
        # Ensure you return these in their correct position: yaani (outside)
        return wrapper
    return decorator

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
@retry_on_failure(retries=3, delays=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)