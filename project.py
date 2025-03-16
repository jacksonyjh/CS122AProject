import sys
import os
import db_utils
from create_table_query import create_table_query_map
from inserts import insert_viewer, add_genre, insert_movie, insert_session, update_release
from deletes import delete_viewer
from selects import select_releases, popular_releases, release_title




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


def load_data(folder_name):
    """Load data into 122A DB"""
    connection = db_utils.connect_to_cs122a()
    if not connection:
        print("Failed to connect to cs122a database.")
        return

    try:
        cursor = connection.cursor()

        # Disable foreign key checks to allow dropping tables
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        # Create each table
        for table_name in table_order:

            # Delete existing tables 
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            # print(f"Deleted {table_name}")

            #Create new tables
            cursor.execute(create_table_query_map[table_name])

            # print(f"Created {table_name} table")

            file_path = os.path.join(folder_name, table_name) + ".csv"

            with open(file_path, 'r') as file:
                # first line is always columns, subsequent rows = data to input
                columns = file.readline()
                
                for line in file:
                    values = line.strip().split(",")
                    query = f"INSERT INTO {table_name} VALUES ({','.join(['%s'] * len(values))})"
                    cursor.execute(query, values)
        print("Success")
    except Exception as e:
        print("Fail")
    connection.commit()
        # print("Data import successful.")
    cursor.close()
    connection.close()

def main():
    if len(sys.argv) < 2:
        print("No function specified.")
        return

    # Initialize the database before running any commands
    if not db_utils.initialize_database():
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

    elif function_name == "addGenre":
        uid = args[0]
        genre = args[1]
        add_genre(uid, genre)

    elif function_name == "deleteViewer":
        uid = args[0]
        delete_viewer(uid)
    
    elif function_name == "insertMovie":
        rid = args[0]
        url = args[1]
        insert_movie(rid, url)

    elif function_name == "insertSession":
        insert_session(*args)

    elif function_name == "updateRelease":
        rid = args[0]
        title = args[1]
        update_release(rid, title)

    elif function_name == "listReleases":
        uid = args[0]
        select_releases(uid)

    elif function_name == "popularRelease":
        num = args[0]
        popular_releases(num)

    elif function_name == "releaseTitle":
        sid = args[0]
        release_title(sid)



    # Add other commands similarly
    else:
        print("Unknown function.")

if __name__ == "__main__":
    main()
