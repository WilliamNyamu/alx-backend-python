# create a reusable context manager that takes a query as input and executes it, 
# managing both connection and the query execution

import sqlite3
from sqlite3 import Error

class ExecuteQuery:
    def __init__(self, query, parameter):
        self.db = sqlite3.connect('users.db')
        self.query = query
        self.parameter = parameter
    
    def __enter__(self):
        return self.db
    
    def __exit__(self, type, value, traceback):
        return self.db.close()

    def __str__(self):
        return self.query

def execute_db(query, parameter):
    with ExecuteQuery(query=query, parameter=parameter) as db:
        try:
            cursor = db.cursor()
            cursor.execute(query, (parameter,))
            results = cursor.fetchall()
            yield results
        except Error as e:
            print(f"Error occured: {e}")

users = execute_db(query="SELECT * FROM users WHERE age > ?", parameter=115)
for user in users:
    print(user)

