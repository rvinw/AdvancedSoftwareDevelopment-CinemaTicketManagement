import sqlite3

def add_user(username, password, forename, surname, usertype):
    con = sqlite3.connect("HorizonCinema.db")
    cur = con.cursor()

    cur.execute('''
    INSERT INTO movie (username, userPassword, userForename, userSurname, userType)
    VALUES (?, ?, ?, ?, ?)
    ''', (username, password, forename, surname, usertype))

    con.commit()
    con.close()
    
username = ''
password = ''
forename = ''
surname = ''
usertype = ''

add_user(username, password, forename, surname, usertype)