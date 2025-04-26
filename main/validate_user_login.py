import sqlite3

def validate_user_login(username, password):
    conn = sqlite3.connect('HorizonCinema.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT usertype FROM staff
        WHERE username = ? AND userPassword = ?
    ''', (username, password))

    result = cursor.fetchone()

    conn.close()

    if result:
        usertype = result[0]
        return usertype
    else:
        return 'Invalid username or password'


def add_booking():
    pass

def cancel_booking():
    pass

print(validate_user_login("normalstaff", "password123"))