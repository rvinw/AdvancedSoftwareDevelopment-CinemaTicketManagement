import sqlite3

def add_screen(cinemaID, screen_name, capacity):
    con = sqlite3.connect("HorizonCinema.db")
    cur = con.cursor()

    cur.execute('''
    INSERT INTO screen (cinemaID, screenName, capacity)
    VALUES (?, ?, ?)
    ''', (cinemaID, screen_name, capacity))

    con.commit()
    con.close()

screens = [['Screen 1', 60],['Screen 2', 70],['Screen 3', 85],['Screen 4', 95],['Screen 5', 105],['Screen 6', 120]]
cinemaID = 1

for i in screens:
    add_screen(cinemaID, i[0], i[1])

