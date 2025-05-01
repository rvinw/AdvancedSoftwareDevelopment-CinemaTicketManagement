# Written By Arvin Valad Khani (23035803)

import sqlite3
from tkinter import messagebox

def insert_default_users():
    default_users = [
        ('BookingStaff', 'Vincent', 'Richardson-Price', 1, 'staffpass123', 1),
        ('Manager', 'Jake', 'Richardson-Price', 2, 'manpass123', 2),
        ('Admin', 'Alex', 'Nakhle', 3, 'adminpass123', 3)
    ]

    conn = sqlite3.connect('HorizonCinema.db')
    cur = conn.cursor()

    for username, forename, surname, usertype, password, cinemaID in default_users:
        cur.execute("SELECT username FROM staff WHERE username = ?", (username,))
        if not cur.fetchone():
            cur.execute('''
                INSERT INTO staff (username, userForename, userSurname, userType, userPassword, cinemaID)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, forename, surname, usertype, password, cinemaID))

    conn.commit()
    conn.close()
    
insert_default_users()

def add_user(username, password, forename, surname, usertype, cinemaID):
    insert_default_users()  # Ensure defaults are inserted only once

    if not all([username, password, forename, surname, usertype]):
        messagebox.showerror("Input Error", "All fields are required.")
        return

    try:
        usertype = int(usertype)
    except ValueError:
        messagebox.showerror("Input Error", "User type must be a number (e.g. 1, 2, 3).")
        return

    try:
        conn = sqlite3.connect("HorizonCinema.db")
        cur = conn.cursor()

        cur.execute("SELECT username FROM staff WHERE username = ?", (username,))
        if cur.fetchone():
            messagebox.showerror("Error", f"Username '{username}' already exists.")
            return

        cur.execute('''
            INSERT INTO staff (username, userForename, userSurname, userType, userPassword, cinemaID)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, forename, surname, usertype, password, int(cinemaID)))

        conn.commit()
        messagebox.showinfo("Success", f"User '{username}' added successfully.")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        conn.close()

