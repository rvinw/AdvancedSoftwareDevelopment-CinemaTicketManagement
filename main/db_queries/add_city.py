import sqlite3
from tkinter import messagebox

def add_city(city_name, base_price):
    city_name = city_name.capitalize()

    # Check if base_price is a valid number
    try:
        base_price = int(base_price)
    except ValueError:
        messagebox.showerror("Error", "Base price must be a valid number.")
        return

    con = sqlite3.connect("HorizonCinema.db")
    cur = con.cursor()

    # Check if city already exists (case-insensitive)
    cur.execute("SELECT cityID FROM city WHERE LOWER(cityName) = ?", (city_name.lower(),))
    if cur.fetchone():
        messagebox.showerror("Error", f"City '{city_name}' already exists. Skipping insertion.")
    else:
        cur.execute('''
            INSERT INTO city (cityName, basePrice)
            VALUES (?, ?)
        ''', (city_name, base_price))
        messagebox.showinfo("Success", f"City '{city_name}' added successfully.")

    con.commit()
    con.close()
    
    return