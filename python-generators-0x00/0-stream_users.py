# create a generator that streams rows from the SQL database
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

def stream_users():
    try:
        with mysql.connector.connect(
            host='localhost',
            user='root',
            password=os.environ.get('password'),
            database = 'ALX_prodev',
        ) as connection:
            with connection.cursor(buffered=True) as cursor: # we put buffered=True to ensure that we don't get the error of Unread result found.
                cursor.execute("SELECT * FROM user_data;")
                # Do not load everything in memory
                for row in cursor:
                    yield row

    except Error as e:
        print(f"Error occured: {e}")