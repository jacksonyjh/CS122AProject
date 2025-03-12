import db_utils
import mysql.connector

def select_releases(uid):
    """Given UID, list releases the viewer has reviewed, in ASC order of titles"""
    connection = db_utils.connect_to_cs122a()
    if not connection:
        print("Failed to connect to cs122a database.")
        return

    cursor = connection.cursor()

    select_releases_query = """
    SELECT releases.rid, releases.genre, releases.title
    FROM releases
    JOIN reviews ON reviews.rid = releases.rid
    WHERE uid = %s
    ORDER BY title ASC;
"""

    cursor.execute(select_releases_query, (uid,))
    results = cursor.fetchall()

    for row in results:
        print(row)

    print(f"{uid}'s releases selected!")

    connection.commit()
    cursor.close()
    connection.close()
    return


def popular_releases(num):
    connection = db_utils.connect_to_cs122a()
    if not connection:
        print("Failed to connect to cs122a database.")
        return

    cursor = connection.cursor()

    pop_releases_query = """
    SELECT releases.rid, releases.title, COUNT(reviews.rvid) AS reviewCount
    FROM releases
    JOIN reviews ON reviews.rid = releases.rid
    GROUP BY releases.rid
    ORDER BY reviewCount DESC, releases.rid;
    LIMIT %s
"""

    cursor.execute(pop_releases_query, (num,))
    results = cursor.fetchall()

    for row in results:
        print(row)

    print(f"top {num} releases selected!")

    connection.commit()
    cursor.close()
    connection.close()
    return