import db_utils
import mysql.connector

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