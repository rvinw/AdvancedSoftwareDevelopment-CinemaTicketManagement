# Written By Arvin Valad Khani (23035803)

import sqlite3
from tkinter import messagebox

def add_cinema(cinema_name, number_of_screens, city_name):
    con = sqlite3.connect("HorizonCinema.db")
    cur = con.cursor()

    city_name = city_name.capitalize()

    cur.execute('SELECT cityID FROM city WHERE cityName = ?', (city_name,))
    result = cur.fetchone()

    if result:
        city_id = result[0]

        cur.execute('''
            INSERT INTO cinema (cinemaName, numberOfScreens, cityID)
            VALUES (?, ?, ?)
        ''', (cinema_name, number_of_screens, city_id))

        con.commit()
        con.close()
        messagebox.showinfo("Success", f"Cinema '{cinema_name}' added to city '{city_name}'.")
        
    else:
        messagebox.showerror("Error", f"City '{city_name}' does not exist in the database. Please add it first.")  
    
    return
