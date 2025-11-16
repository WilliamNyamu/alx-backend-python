# create a decorator that will caches the results of a database queries inorder to avoid redundant calls

import time
import functools
import sqlite3
from sqlite3 import Error

query_cache = {}

# Use the cache key and its results as the value. This will help in querying
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Retrieve the cache_key from the query argument passed
        cache_key = kwargs.get('query')

        # Check whether the cache_key exists and then return the results it has instead.
        if cache_key in query_cache:
            return query_cache[cache_key]
        
        try:
            # Run the function
            items = func(*args, **kwargs)
            query_cache[cache_key] = items # Store the cache_key and its results in the query_cache db
            return items
        except Error as e:
            print(f"Error occured: {e}")
    return wrapper

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
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users LIMIT 5")


#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")

print(users_again)