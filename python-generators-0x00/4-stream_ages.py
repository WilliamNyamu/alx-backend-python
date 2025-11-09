# Script that yields user ages one by one and then calculates the average age without loading the whole dataset to memory
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import statistics

load_dotenv()

def stream_user_ages():
    try:
        with mysql.connector.connect(
            host="localhost",
            user='root',
            password=os.environ.get('password'),
            database='ALX_prodev'
        ) as connection:
                with connection.cursor(dictionary=True, buffered=False) as cursor:
                    cursor.execute("SELECT name, age FROM user_data;")
                    for user in cursor:
                         yield user
    except Error as e:
         print(f"Error occured: {e}")

# It could have been so easy to tackle the problem by initializing an empty list, appending values to it 
# and then calculating the average. This would have meant loading everything in memory
# So use the method below to ensure it is still memory efficient

def calculate_average():
     total, count = 0, 0
     for person in stream_user_ages():
          total += person['age']
          count +=1
     if count > 0:
          print(f"Average age of users: {total/count}")
     else:
          print("You encountered an error")

calculate_average()