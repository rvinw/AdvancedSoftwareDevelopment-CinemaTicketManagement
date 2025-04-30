import sqlite3
from datetime import datetime
from tkinter import messagebox


def add_screen(cinema_id, screen_name, capacity):
    try:
        capacity = int(capacity)
    except ValueError:
        return "Capacity must be a number."

    con = sqlite3.connect("HorizonCinema.db")
    cur = con.cursor()

    # Optional: Check if screen already exists
    cur.execute("SELECT * FROM screen WHERE screenName = ? AND cinemaID = ?", (screen_name, cinema_id))
    if cur.fetchone():
        con.close()
        return f"Screen '{screen_name}' already exists for this cinema."

    cur.execute('''
        INSERT INTO screen (cinemaID, screenName, capacity)
        VALUES (?, ?, ?)
    ''', (cinema_id, screen_name, capacity))

    con.commit()
    con.close()
    return "Screen added successfully."

def get_all_screens():
    con = sqlite3.connect("HorizonCinema.db")
    cur = con.cursor()

    cur.execute("SELECT screenID, cinemaID, screenName, capacity FROM screen")
    screens = cur.fetchall()

    con.close()
    return screens