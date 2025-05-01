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
    
    if valid:
        con = sqlite3.connect("HorizonCinema.db")
        cur = con.cursor()

        cur.execute('''
        INSERT INTO show (movieID, showDateTime, screenID)
        VALUES (?, ?, ?)
        ''', (movieID, showDateTime, screenID))

        con.commit()
        con.close()
    
    else:
        messagebox.showerror("Invalid DateTime", result)