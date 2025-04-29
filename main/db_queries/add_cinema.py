import sqlite3

def add_cinema(cinema_name, cityID):
    con = sqlite3.connect("HorizonCinema.db")
    cur = con.cursor()

    cur.execute('''
    INSERT INTO cinema (cinemaName, cityID)
    VALUES (?, ?)
    ''', (cinema_name, cityID))

    con.commit()
    con.close()
    
name = 'London II'
cityID = 4


add_cinema(name, cityID)