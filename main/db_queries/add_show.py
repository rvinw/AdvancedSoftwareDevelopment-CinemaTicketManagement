import sqlite3
from datetime import datetime
from tkinter import messagebox

def validate_datetime(dt_string):
    try:
        dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M")
        if dt < datetime.now():
            return False, "Date/time cannot be in the past."
        return True, dt
    except ValueError:
        return False, "Invalid date/time format. Use YYYY-MM-DD HH:MM"

def add_show(movieID, showDateTime, screenID):
    valid, result = validate_datetime(showDateTime)

    if not valid:
        messagebox.showerror("Invalid DateTime", result)
        return

    con = sqlite3.connect("HorizonCinema.db")
    cur = con.cursor()

    # Check for collision: is there already a show on this screen at this datetime?
    cur.execute('''
        SELECT * FROM show
        WHERE screenID = ? AND showDateTime = ?
    ''', (screenID, showDateTime))

    collision = cur.fetchone()

    if collision:
        con.close()
        messagebox.showerror("Show Collision", "There is already a show scheduled on this screen at this time.")
        return

    # No collision, proceed to insert
    cur.execute('''
        INSERT INTO show (movieID, showDateTime, screenID)
        VALUES (?, ?, ?)
    ''', (movieID, showDateTime, screenID))

    con.commit()
    con.close()
    messagebox.showinfo("Success", "Show added successfully.")