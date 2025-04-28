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
        return result[0]  # usertype
    else:
        return None



def add_booking():
    pass

def cancel_booking():
    pass

#print(validate_user_login("normalstaff", "password123"))