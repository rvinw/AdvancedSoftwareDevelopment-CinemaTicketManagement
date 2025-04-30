import sqlite3
from tkinter import messagebox

def insert_default_users():
    default_users = [
        ('BookingStaff', 'Vincent', 'Richardson-Price', 1, 'staffpass123'),
        ('Manager', 'Jake', 'Richardson-Price', 2, 'manpass123'),
        ('Admin', 'Alex', 'Nakhle', 3, 'adminpass123')
    ]

    conn = sqlite3.connect('HorizonCinema.db')
    cur = conn.cursor()

    for username, forename, surname, usertype, password in default_users:
        cur.execute("SELECT username FROM staff WHERE username = ?", (username,))
        if not cur.fetchone():
            cur.execute('''
                INSERT INTO staff (username, userForename, userSurname, userType, userPassword)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, forename, surname, usertype, password))

    conn.commit()
    conn.close()

def add_user(username, password, forename, surname, usertype):
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
            INSERT INTO staff (username, userForename, userSurname, userType, userPassword)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, forename, surname, usertype, password))

        conn.commit()
        messagebox.showinfo("Success", f"User '{username}' added successfully.")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        conn.close()

