import mysql.connector
import sys
import os


# lowk might hard code these create table queries (source: homework 2 solutions)
create_table_query_map = dict()
create_table_query_map["users"] = """CREATE TABLE Users (
    uid INT,
    email TEXT NOT NULL,
    joined_date DATE NOT NULL,
    nickname TEXT NOT NULL,
    street TEXT,
    city TEXT,
    state TEXT,
    zip TEXT,
    genres TEXT,
    PRIMARY KEY (uid)
);
"""

create_table_query_map["producers"] = """CREATE TABLE Producers (
    uid INT,
    bio TEXT,
    company TEXT,
    PRIMARY KEY (uid),
    FOREIGN KEY (uid) REFERENCES Users(uid) ON DELETE CASCADE
);
"""


create_table_query_map["viewers"] = """CREATE TABLE Viewers (
    uid INT,
    subscription ENUM('free', 'monthly', 'yearly'),
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    PRIMARY KEY (uid),
    FOREIGN KEY (uid) REFERENCES Users(uid) ON DELETE CASCADE
);
"""
create_table_query_map["releases"] = """CREATE TABLE Releases (
    rid INT,
    producer_uid INT NOT NULL,
    title TEXT NOT NULL,
    genre TEXT NOT NULL,
    release_date DATE NOT NULL,
    PRIMARY KEY (rid),
    FOREIGN KEY (producer_uid) REFERENCES Producers(uid) ON DELETE CASCADE
);
"""

create_table_query_map["movies"] = """CREATE TABLE Movies (
    rid INT,
    website_url TEXT,
    PRIMARY KEY (rid),
    FOREIGN KEY (rid) REFERENCES Releases(rid) ON DELETE CASCADE
);
"""

create_table_query_map["series"] = """CREATE TABLE Series (
    rid INT,
    introduction TEXT,
    PRIMARY KEY (rid),
    FOREIGN KEY (rid) REFERENCES Releases(rid) ON DELETE CASCADE
);
"""
create_table_query_map["videos"] = """CREATE TABLE Videos (
    rid INT,
    ep_num INT NOT NULL,
    title TEXT NOT NULL,
    length INT NOT NULL,
    PRIMARY KEY (rid, ep_num),
    FOREIGN KEY (rid) REFERENCES Releases(rid) ON DELETE CASCADE
);
"""
create_table_query_map["sessions"] = """CREATE TABLE Sessions (
    sid INT,
    uid INT NOT NULL,
    rid INT NOT NULL,
    ep_num INT NOT NULL,
    initiate_at DATETIME NOT NULL,
    leave_at DATETIME NOT NULL,
    quality ENUM('480p', '720p', '1080p'),
    device ENUM('mobile', 'desktop'),
    PRIMARY KEY (sid),
    FOREIGN KEY (uid) REFERENCES Viewers(uid) ON DELETE CASCADE,
    FOREIGN KEY (rid, ep_num) REFERENCES Videos(rid, ep_num) ON DELETE CASCADE
);
"""

create_table_query_map["reviews"] = """CREATE TABLE Reviews (
    rvid INT,
    uid INT NOT NULL,
    rid INT NOT NULL,
    rating DECIMAL(2, 1) NOT NULL CHECK (rating BETWEEN 0 AND 5),
    body TEXT,
    posted_at DATETIME NOT NULL,
    PRIMARY KEY (rvid),
    FOREIGN KEY (uid) REFERENCES Viewers(uid) ON DELETE CASCADE,
    FOREIGN KEY (rid) REFERENCES Releases(rid) ON DELETE CASCADE
);
"""


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
