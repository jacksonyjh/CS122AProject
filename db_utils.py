import mysql.connector

def connect_to_server():
    """Connect to MYSQL Server"""
    try:
        connection = mysql.connector.connect(
            user='test',
            password='password',
            host='localhost',
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def initialize_database():
    """Create 122A DB if needed"""
    connection = connect_to_server()
    if not connection:
        # print("Failed to connect to MySQL.")
        return False

    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS cs122a")
        cursor.close()
        connection.close()
        # print("Database initialized successfully.")
        return True
    except mysql.connector.Error as err:
        # print(f"Error during database initialization: {err}")
        return False

def connect_to_cs122a():
    """Connect directly to the `cs122a` database."""
    try:
        connection = mysql.connector.connect(
            user='test',    
            password='password',
            host='localhost',
            database='cs122a'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
