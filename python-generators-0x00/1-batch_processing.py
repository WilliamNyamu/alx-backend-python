# generator to fetch and process data in batches from the users database
# use def batch_processing(batch_size) that processes each batch to filter users over the age of 25
# use def stream_users_in_batches(batch_size)
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()


def stream_users_in_batches(batch_size):
    try:
        with mysql.connector.connect(
            host='localhost',
            user='root',
            password=os.environ.get('password'),
            database='ALX_prodev'
        ) as connection:
            with connection.cursor(dictionary=True) as cursor: # we use dictionary=True to return a dictionary instead of a tuple
                cursor.execute("SELECT * FROM user_data;")
                while True:
                    batch = cursor.fetchmany(batch_size)
                    if not batch:
                        break
                    yield batch
                
    except Error as e:
        print(f"Error occured: {e}")

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size=batch_size):
        for row in batch:
            if row['age'] > 25:
                print(row)
