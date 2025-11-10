# create a decorator that automatically handles opening and closing database connections

import sqlite3
import functools
from sqlite3 import Error

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            connection = sqlite3.connect('users.db')
            value = func(connection, *args, **kwargs)
            connection.close()
            return value
        except Error as e:
            print(f"Error occured: {e}")
    return wrapper

@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) 
    return cursor.fetchone() 
    #### Fetch user by ID with automatic connection handling 

user = get_user_by_id(user_id=1)
print(user)