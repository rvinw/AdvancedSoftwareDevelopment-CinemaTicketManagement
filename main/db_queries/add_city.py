import sqlite3

def add_city(city_name, base_price):
    con = sqlite3.connect("HorizonCinema.db")
    cur = con.cursor()

    cur.execute('''
    INSERT INTO city (cityName, basePrice)
    VALUES (?, ?)
    ''', (city_name, base_price))

    con.commit()
    con.close()
    
city_name = 'London'
base_price = 10

add_city(city_name, base_price)