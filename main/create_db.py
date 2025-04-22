import sqlite3

con = sqlite3.connect("HorizonCineama.db")
cur = con.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS staff (
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    userForename TEXT NOT NULL UNIQUE,
    userSurname TEXT NOT NULL UNIQUE,
    userType INTEGER NOT NULL CHECK(usertype IN (1, 2, 3)),
    userPassword TEXT NOT NULL
)
''')

cur.execute('''
INSERT INTO staff (username, userForename, userSurname, userType, userPassword)
VALUES (?, ?, ?, ?, ?)
''', ('normalstaff', 'Arvin', 'Valad', 1, 'password123'))

con.commit()
con.close()