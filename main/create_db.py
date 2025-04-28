import sqlite3

con = sqlite3.connect("HorizonCinema.db")
cur = con.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS staff (
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    userForename TEXT NOT NULL,
    userSurname TEXT NOT NULL,
    userType INTEGER NOT NULL CHECK(userType IN (1, 2, 3)),
    userPassword TEXT NOT NULL
)
''')

cur.executemany('''
INSERT INTO staff (username, userForename, userSurname, userType, userPassword)
    VALUES (?, ?, ?, ?, ?)
''', [
    ('normalstaff', 'Arvin', 'Valad', 1, 'password123'),
    ('BookingStaff', 'Vincent', 'Richardson-Price', 1, 'staffpass123'),
    ('Manager', 'Jake', 'Richardson-Price', 2, 'manpass123'),
    ('Admin', 'Alex', 'Nakhle', 3, 'adminpass123')
])



cur.execute('''
CREATE TABLE IF NOT EXISTS movie (
    movieID INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    genre TEXT NOT NULL,
    age TEXT NOT NULL,
    rating FLOAT NOT NULL,
    director TEXT NOT NULL,
    cast TEXT NOT NULL
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS city (
    cityID INTEGER PRIMARY KEY AUTOINCREMENT,
    cityName TEXT NOT NULL UNIQUE,
    basePrice INTEGER NOT NULL
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS cinema (
    cinemaID INTEGER PRIMARY KEY AUTOINCREMENT,
    cinemaName TEXT NOT NULL,
    cityID INTEGER NOT NULL,
    FOREIGN KEY (cityID) REFERENCES city(cityID)
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS screen (
    screenID INTEGER PRIMARY KEY AUTOINCREMENT,
    cinemaID INTEGER NOT NULL UNIQUE,
    capacity INTEGER NOT NULL,
    FOREIGN KEY (cinemaID) REFERENCES cinema(cinemaID)
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS show (
    showID INTEGER PRIMARY KEY AUTOINCREMENT,
    movieID INTEGER NOT NULL,
    showTime TEXT NOT NULL,
    screenID INTEGER NOT NULL,
    FOREIGN KEY (movieID) REFERENCES movie(movieID),
    FOREIGN KEY (screenID) REFERENCES screen(screenID)
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS seat (
    seatID INTEGER NOT NULL,
    seatType TEXT NOT NULL,
    screenID INTEGER NOT NULL,
    PRIMARY KEY (seatID, screenID),
    FOREIGN KEY (screenID) REFERENCES screen(screenID)
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS booking (
    bookingID INTEGER NOT NULL,
    showID INTEGER NOT NULL,
    seatID INTEGER NOT NULL,
    price FLOAT NOT NULL,
    cancelled BOOLEAN DEFAULT 0,
    PRIMARY KEY (bookingID, seatID),
    FOREIGN KEY (showID) REFERENCES show(showID),
    FOREIGN KEY (seatID) REFERENCES seat(seatID)
)
''')

con.commit()
con.close()