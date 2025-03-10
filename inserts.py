import db_utils
import mysql.connector

def insert_viewer(*args):
    """Inserts a User and Viewer into their respective tables"""
    connection = db_utils.connect_to_cs122a()
    if not connection:
        print("Failed to connect to cs122a database.")
        return

    cursor = connection.cursor()

    uid = args[0]
    email = args[1]
    nickname = args[2]
    street = args[3]
    city = args[4]
    state = args[5]
    zipcode = args[6]
    genres = args[7]
    joined_date = args[8]
    first_name = args[9]
    last_name = args[10]
    subscription = args[11]

    # add user only if it doesn't already exist
    try:
        users_query = """INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        viewers_query = """INSERT INTO viewers VALUES (%s, %s, %s, %s)"""
        cursor.execute(users_query, (uid, email, joined_date, nickname, street, city, state, zipcode, genres))
        cursor.execute(viewers_query, (uid, subscription, first_name, last_name))
        
    
        print("User added")
        print("Viewer added")
    
    except mysql.connector.IntegrityError as e:
        print("Fail: Duplicate ID for Users/Viewers")



    # try:

        # I ASKED ON ED WAITING ON RESPONSE
        #(if they have same uid on both Users and Viewers,
        # but different names, i feel like the insert query should fail (?))

        # HII UPDATE (ill finish this later)

        # This is from the TA
        # If the uid already exists in the users table, you are supposed to return Fail in this case.
        # We are assuming that we are creating both a new User and new Viewer;
        # if the User and/or Viewer already exists, you should return Fail.

        # user already exists

    connection.commit()
    cursor.close()
    connection.close()
    
    
    
def add_genre(uid, genre):
    """Adds a genre to a User's genre list"""
    connection = db_utils.connect_to_cs122a()
    if not connection:
        print("Failed to connect to cs122a database.")
        return

    cursor = connection.cursor()

    try:
        extract_genres_query = """SELECT genres FROM users WHERE uid = %s"""
        cursor.execute(extract_genres_query, (uid,))

        # check if user exists
        genres = cursor.fetchone()
        if genres is None:
            raise ValueError("UID does not exist, Fail")

        genre_list = genres[0].split(";")
        
        # check if genre already exists before adding
        for gen in genre_list:
            if (gen.lower() == genre.lower()):
                raise ValueError(f"Genre already exists for UID {uid}, Fail")
        
        genre_list.append(genre)

        update_genre_query = """UPDATE users SET genres = %s WHERE uid = %s"""

        cursor.execute(update_genre_query, (";".join(genre_list), uid,))
        print("Genres updated!")
    
    except ValueError as e:
        print(e)

    connection.commit()
    cursor.close()
    connection.close()


def insert_movie(rid, url):
    """Inserts Movie into Movies Table"""
    connection = db_utils.connect_to_cs122a()
    if not connection:
        print("Failed to connect to cs122a database.")
        return

    cursor = connection.cursor()

    try:
        insert_movie_query = "INSERT INTO movies VALUES (%s, %s)"
        cursor.execute(insert_movie_query, (rid, url,))
        print(f"added rid {rid}")
    except mysql.connector.IntegrityError as e:
        print(f"rid {rid} already exists, failed to insert")
    
    connection.commit()
    cursor.close()
    connection.close()


def insert_session(*args):
    """Creates a session for specific viewer"""
    connection = db_utils.connect_to_cs122a()
    if not connection:
        print("Failed to connect to cs122a database.")
        return

    cursor = connection.cursor()

    sid = args[0]
    uid = args[1]
    rid = args[2]
    ep_num = args[3]
    init_at = args[4]
    leave_at = args[5]
    quality = args[6]
    device = args[7]

    try:

        create_sesh_query = "INSERT INTO sessions VALUES (%s,%s,%s,%s,%s,%s,%s, %s)"
        cursor.execute(create_sesh_query, (sid, uid, rid, ep_num, init_at, leave_at, quality, device,))
        
        print(f"sid {sid} created")

    except mysql.connector.IntegrityError as e:
        print("Duplicate SID provided. Fail")

    connection.commit()
    cursor.close()
    connection.close()


    
def update_release(rid, title):
    """Updates the Title of a Release"""
    connection = db_utils.connect_to_cs122a()
    if not connection:
        print("Failed to connect to cs122a database.")
        return

    cursor = connection.cursor()

    update_release_query = "UPDATE releases SET title = %s WHERE rid = %s"
    cursor.execute(update_release_query, (title, rid,))

    print(f"rid {rid} title updated")

    connection.commit()
    cursor.close()
    connection.close()

    return