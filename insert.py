def insert_viewer(*args):
    connection = connect_to_cs122a()
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
    genre = args[7]
    joined_date = args[8]
    first_name = args[9]
    last_name = args[10]
    subscription = args[11]

    query = """INSERT INTO viewers VALUES 
    (uid, email, nickname, street, city, state, 
    zipcode, genre, joined_date, first_name, last_name, subscription)"""

    cursor.execute(query)
    
    
