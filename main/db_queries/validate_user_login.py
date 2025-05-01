# Written By Arvin Valad Khani (23035803)

import sqlite3

def validate_user_login(username, password):
    con = sqlite3.connect('HorizonCinema.db')
    cur = con.cursor()

    # Assuming you have a table 'staff' with columns 'username' and 'userPassword'
    cur.execute('''
        SELECT userType FROM staff WHERE username = ? AND userPassword = ?
    ''', (username, password))

    result = cur.fetchone()
    con.close()

    # If result is found, return the userType (1, 2, or 3)
    if result:
        return result[0]  # userType, which should be 1, 2, or 3
    else:
        return None  # No valid match



#print(validate_user_login("normalstaff", "password123"))