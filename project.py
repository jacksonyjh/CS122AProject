import mysql.connector
import sys
import os


# db = mysql.connector.connect(
#     host = "localhost",
#     user = "test",
#     password = "password",
#     database = "cs122a"
# )

# cursor = db.cursor()

# cursor.execute("CREATE TABLE ")
# cursor.execute("CREATE DATABASE IF NOT EXISTS cs122a")

def connect_to_server():
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
    elif function_name == "insertViewer":
        insert_viewer(*args)
    # Add other commands similarly
    else:
        print("Unknown function.")

def create_table_query(cols table_name,):
    """Takes in string list columns and tablename, returns query to create table for DB"""
    id = cols[0] # first index always id
    query  = f"CREATE TABLE {table_name} ("




def load_data(folder_name):
    connection = connect_to_cs122a()
    if not connection:
        print("Failed to connect to cs122a database.")
        return

    cursor = connection.cursor()

    # Delete existing tables and recreate them
    # Execute the provided DDLs
    # For example:
    # cursor.execute("DROP TABLE IF EXISTS table_name")
    # cursor.execute("""
    #     CREATE TABLE table_name (
    #         column1 datatype,
    #         column2 datatype,
    #         ...
    #     )
    # """)

    # Load CSV files into tables
    for filename in os.listdir(folder_name):
        table_name = filename.split('.')[0]
        print("TABLE NAME: ", table_name)
        file_path = os.path.join(folder_name, filename)
        print(f"Loading data from {file_path} into table {table_name}.")
        with open(file_path, 'r') as file:
            column_names = file.readline().strip("\n").split(",")
            print("Columns: ", column_names)

            create_table(column_names, table_name)

            # cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{col} VARCHAR(255)' for col in column_names])});")

            print("CREATED TABLE: ", table_name)
            for line in file:
                values = line.strip().split(',')
                print(values)
                # Use prepared statements for insertion
                query = f"INSERT INTO {table_name} VALUES ({','.join(['%s'] * len(values))})"
                cursor.execute(query, values)

    # connection.commit()
    print("Data import successful.")
    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
