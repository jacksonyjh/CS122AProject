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
    
    
    
