import mysql.connector
import sys
import os
from create_table_query import create_table_query_map


table_order = [
        "users",
        "producers",
        "viewers",
        "releases",
        "movies",
        "series",
        "videos",
        "sessions",
        "reviews"
    ]

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
        print("Failed to connect to MySQL.")
        return False

    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS cs122a")
        cursor.close()
        connection.close()
        print("Database initialized successfully.")
        return True
    except mysql.connector.Error as err:
        print(f"Error during database initialization: {err}")
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

def load_data(folder_name):
    """Load data into 122A DB"""
    connection = connect_to_cs122a()
    if not connection:
        print("Failed to connect to cs122a database.")
        return

    cursor = connection.cursor()

    # Disable foreign key checks to allow dropping tables
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    # Create each table
    for table_name in table_order:

        # Delete existing tables 
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        print(f"Deleted {table_name}")

        #Create new tables
        cursor.execute(create_table_query_map[table_name])

        print(f"Created {table_name} table")

        file_path = os.path.join(folder_name, table_name) + ".csv"

        with open(file_path, 'r') as file:
            # first line is always columns, subsequent rows = data to input
            columns = file.readline()
            
            for line in file:
                values = line.strip().split(",")
                query = f"INSERT INTO {table_name} VALUES ({','.join(['%s'] * len(values))})"
                cursor.execute(query, values)
    connection.commit()
    print("Data import successful.")
    cursor.close()
    connection.close()

def main():
    if len(sys.argv) < 2:
        print("No function specified.")
        return

    # Initialize the database before running any commands
    if not initialize_database():
        print("Database initialization failed.")
        return

    function_name = sys.argv[1]
    args = sys.argv[2:]

    # Dispatch functions based on command
    if function_name == "import":
        folder_name = args[0]
        load_data(folder_name)
    # elif function_name == "insertViewer":
    #     insert_viewer(*args)
    # Add other commands similarly
    else:
        print("Unknown function.")

if __name__ == "__main__":
    main()
