import functools
import sqlite3
from sqlite3 import Error


def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            value = func(conn, *args, **kwargs)
            conn.commit()  # Commit if successful
            return value
        except Error as e:
            conn.rollback()  # Rollback on error
            print(f"Error occurred: {e}")
            raise  # Re-raise so caller knows it failed
    return wrapper


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        connection = None
        try:
            connection = sqlite3.connect('users.db')
            # Pass connection as first argument
            value = func(connection, *args, **kwargs)
            return value
        except Error as e:
            print(f"Error occurred: {e}")
            raise
        finally:
            if connection:
                connection.close()
    return wrapper


@with_db_connection
@transactional 
def update_user_email(conn, name, new_email):
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE name = ?", (new_email, name))


# Now call without conn (it's provided by decorator)
update_user_email(name='Johnnie Mayer', new_email='Crawford_Cartwright@hotmail.com')
print(update_user_email)