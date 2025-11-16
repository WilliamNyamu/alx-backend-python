# create a class based context manager to handle opening and closing database connections automatically
import sqlite3
from sqlite3 import Error


class DatabaseConnection:
    def __init__(self):
        self.db = sqlite3.connect('users.db')
    
    def __enter__(self):
        return self.db
    
    def __exit__(self, type, value, traceback):
        return self.db.close()

def calling_db():
    with DatabaseConnection() as db:
        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
            yield results
        except Error as e:
            print(f"Error occured: {e}")

users = calling_db()
for user in users:
    print(user)
