import sqlite3

def add_user(username, password, forename, surname, usertype):
    con = sqlite3.connect("HorizonCinema.db")
    cur = con.cursor()

    #cur.execute('''
    #INSERT INTO movie (username, userPassword, userForename, userSurname, userType)
    #VALUES (?, ?, ?, ?, ?)
    #''', (username, password, forename, surname, usertype))
    
    conn = sqlite3.connect('HorizonCinema.db')
    cur = conn.cursor()
    cur.executemany('''
    INSERT INTO staff (username, userForename, userSurname, userType, userPassword)
        VALUES (?, ?, ?, ?, ?)
    ''', [
        ('BookingStaff', 'Vincent', 'Richardson-Price', 1, 'staffpass123'),
        ('Manager', 'Jake', 'Richardson-Price', 2, 'manpass123'),
        ('Admin', 'Alex', 'Nakhle', 3, 'adminpass123')
    ])

    conn.commit()  # This actually saves the changes
    conn.close()

    #con.commit()
    #con.close()
    
username = ''
password = ''
forename = ''
surname = ''
usertype = ''

add_user(username, password, forename, surname, usertype)

