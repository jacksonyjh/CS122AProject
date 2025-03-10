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

    try:
        users_query = """INSERT INTO users VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(users_query, (uid, email, joined_date, nickname, street, city, state, zipcode, genres))
        print("User added")
    
    except mysql.connector.IntegrityError as e:
        print("Error: ", e)
        print("Failed to add user, user with this ID already exists")


    try:
        
        nickname_and_email_query = """SELECT nickname, email FROM Users WHERE uid = (%s)"""
        cursor.execute(nickname_and_email_query, (uid,))
        user_nickname, user_email = cursor.fetchone()



        # I ASKED ON ED WAITING ON RESPONSE
        #(if they have same uid on both Users and Viewers,
        # but different names, i feel like the insert query should fail (?))
        if (user_nickname != nickname or user_email != email):
            raise ValueError("Error: User already exists with different name")

        viewers_query = """INSERT INTO viewers VALUES 
        (%s, %s, %s, %s)"""
        cursor.execute(viewers_query, (uid, subscription, first_name, last_name))
        print("Viewer added")

    except mysql.connector.IntegrityError as e:
        print("Error: ", e)
        print("Failed to add viewer, viewer with this ID already exists")

    except ValueError as e:
        print("Error: ", e)
        print("Failed to add to viewer") # TEMPORARY
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
            raise ValueError("UID does not exist")

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