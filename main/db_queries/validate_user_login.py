import sqlite3

def validate_user_login(username, password):
    conn = sqlite3.connect('HorizonCinema.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT usertype, userForenmae FROM staff
        WHERE username = ? AND userPassword = ?
    ''', (username, password))

    result = cursor.fetchone()

    conn.close()

    if result:
        usertype = result[0]
        user_forename = result[1]
        return usertype, user_forename
    else:
        return 'Invalid username or password'



#print(validate_user_login("normalstaff", "password123"))