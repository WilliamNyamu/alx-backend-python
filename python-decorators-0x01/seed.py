import sqlite3
from sqlite3 import Error
import csv
import uuid

def connect_to_db():
    try:
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id, name, email, age)")
        connection.close()
    except Error as e:
        print(f"Error occured: {e}")

connect_to_db()

def seed_data():
    try:
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        with open('user_data.csv', 'r') as file_name:
            file = csv.DictReader(file_name)

            insert_query = """
            INSERT OR IGNORE INTO users
            (user_id, name, email, age)
            VALUES( ?, ?, ?, ?)
            """
            for row in file:
                generated_uuid = str(uuid.uuid4())
                cursor.execute(insert_query, (
                    generated_uuid,
                    row['name'],
                    row['email'],
                    int(row['age'])
                ))
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error occured: {e}")
    except FileNotFoundError as f:
        print(f"File not found {f}")
            
        
seed_data()