
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import csv
import os
import uuid

load_dotenv()


def connect_db():
    """Connect to MySQL server (not to a specific database yet)"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # or another user
            password=os.environ.get('password')  # or from environment variable
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_database(connection):
    """Create the ALX_prodev database if it doesn't exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        cursor.close()
        print("Database created successfully")
    except Error as e:
        print(f"Error creating database: {e}")

def connect_to_prodev():
    """Connect specifically to the ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=os.environ.get('password'),
            database='ALX_prodev'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None

def create_table(connection):
    """Create the user_data table"""
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age INT
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")

def insert_data(connection, csv_file):
    """Read data from CSV and insert into user_data table"""
    try:
        cursor = connection.cursor()
        
        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file)
            
            insert_query = """
            INSERT INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE name=name;
            """
            
            for row in csv_reader:
                generated_uuid = str(uuid.uuid4())

                cursor.execute(insert_query, (
                    generated_uuid,
                    row['name'],
                    row['email'],
                    int(row['age'])
                ))
        
        connection.commit()
        cursor.close()
        print(f"Data inserted successfully from {csv_file}")
    except Error as e:
        print(f"Error inserting data: {e}")
    except FileNotFoundError:
        print(f"CSV file {csv_file} not found")