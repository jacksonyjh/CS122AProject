import db_utils
import mysql.connector

def delete_viewer(uid):
    """Deletes a Viewer from Viewer Table"""
    connection = db_utils.connect_to_cs122a()
    if not connection:
        print("Failed to connect to cs122a database.")
        return

    cursor = connection.cursor()

    delete_query = """DELETE FROM viewers WHERE uid = %s"""
    cursor.execute(delete_query, (uid,))
    print(f"Deleted uid {uid}")

    connection.commit()
    cursor.close()
    connection.close()
    return
