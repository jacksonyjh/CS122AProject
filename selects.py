import db_utils
import mysql.connector

# 8 
def list_releases(uid):
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
        print(','.join(map(str, row)))
        # print(row)

    # print(f"{uid}'s releases selected!")

    connection.commit()
    cursor.close()
    connection.close()
    return

# 9
def popular_releases(num):
    connection = db_utils.connect_to_cs122a()
    if not connection:
        print("Fail")
        return

    cursor = connection.cursor()

    num = int(num)
    pop_releases_query = """
    SELECT releases.rid, releases.title, COUNT(reviews.rvid) AS reviewCount
    FROM releases
    JOIN reviews ON reviews.rid = releases.rid
    GROUP BY releases.rid
    ORDER BY reviewCount DESC, releases.rid DESC
    LIMIT %s;
"""

    cursor.execute(pop_releases_query, (num,))
    results = cursor.fetchall()

    for row in results:
        print(','.join(map(str, row)))
        # print(row)

    # print(f"top {num} releases selected!")

    connection.commit()
    cursor.close()
    connection.close()
    return

# 10
def release_title(sid):
    connection = db_utils.connect_to_cs122a()
    if not connection:
        print("Fail")
        return

    cursor = connection.cursor()

    pop_releases_query = """
    SELECT releases.rid, releases.title, releases.genre, videos.title, videos.ep_num, videos.length
    FROM sessions
    JOIN videos ON sessions.rid = videos.rid AND sessions.ep_num = videos.ep_num
    JOIN releases ON videos.rid = releases.rid
    WHERE sessions.sid = %s
    ORDER BY releases.title ASC;
"""

    cursor.execute(pop_releases_query, (sid,))
    results = cursor.fetchall()

    for row in results:
        print(','.join(map(str, row)))
        # print(row)

    # print(f"{sid} releases selected!")

    connection.commit()
    cursor.close()
    connection.close()
    return

# 11
def active_viewer(n, start, end):
    """Returns all active viewers that have started a session more than n times for a time range,
    in ASC order of uid"""
    connection = db_utils.connect_to_cs122a()
    if not connection:
        print("Fail")
        return

    cursor = connection.cursor()

    # n = int(n)
    # print(n)
    # print(start)
    # print(end)

    active_viewer_query = """
    SELECT viewers.uid, viewers.first_name, viewers.last_name
    FROM viewers
    JOIN sessions ON sessions.uid = viewers.uid
    WHERE sessions.initiate_at >= %s AND sessions.leave_at <= %s
    GROUP BY viewers.uid
    HAVING COUNT(sessions.sid) >= %s
    ORDER BY viewers.uid ASC
    """

    cursor.execute(active_viewer_query, (start, end, n,))

    results = cursor.fetchall()

    for row in results:
        print(','.join(map(str, row)))

# 12
def videos_viewed(rid):
    """Given Video rid, count number of UNIQUE viewers that have started a session on it
    Videos not streamed by any viewer have count of 0 instead of NULL"""
    connection = db_utils.connect_to_cs122a()
    if not connection:
        print("Fail")
        return

    cursor = connection.cursor()

    videos_viewed_query = """
    SELECT videos.rid, videos.ep_num, videos.title, videos.length, COUNT(DISTINCT sessions.uid) AS unique_viewers
    FROM videos
    LEFT JOIN sessions ON sessions.rid = videos.rid
    WHERE videos.rid = %s
    GROUP BY videos.rid, videos.ep_num, videos.title, videos.length
    ORDER BY videos.rid DESC
    """

    cursor.execute(videos_viewed_query, (rid, ))

    results = cursor.fetchall()

    
    for row in results:
        print(','.join(map(str, row)))