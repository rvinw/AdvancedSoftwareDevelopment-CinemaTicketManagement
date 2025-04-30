import sqlite3
from tkinter import messagebox
from datetime import datetime, timedelta

def add_booking(showID, seatIDs, staffID):
    try:
        conn = sqlite3.connect("HorizonCinema.db")
        cur = conn.cursor()

        # Get show datetime
        cur.execute("SELECT showDateTime FROM show WHERE showID = ?", (showID,))
        show_row = cur.fetchone()
        if not show_row:
            messagebox.showerror("Error", "Invalid show selected.")
            conn.close()
            return

        try:
            show_datetime = datetime.strptime(show_row[0], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            show_datetime = datetime.strptime(show_row[0], "%Y-%m-%d %H:%M")

        now = datetime.now()

        if show_datetime < now:
            messagebox.showerror("Error", "Cannot book tickets for past shows.")
            conn.close()
            return
        if show_datetime > now + timedelta(days=7):
            messagebox.showerror("Error", "Bookings can only be made up to one week in advance.")
            conn.close()
            return

        # Get screenID
        cur.execute("SELECT screenID FROM show WHERE showID = ?", (showID,))
        screen_row = cur.fetchone()
        if not screen_row:
            conn.close()
            raise ValueError("Invalid showID")
        screenID = screen_row[0]

        # Get cinemaID
        cur.execute("SELECT cinemaID FROM screen WHERE screenID = ?", (screenID,))
        cinema_row = cur.fetchone()
        if not cinema_row:
            conn.close()
            raise ValueError("Screen not found")
        cinemaID = cinema_row[0]

        # Get cityID
        cur.execute("SELECT cityID FROM cinema WHERE cinemaID = ?", (cinemaID,))
        city_row = cur.fetchone()
        if not city_row:
            conn.close()
            raise ValueError("Cinema not found")
        cityID = city_row[0]

        # Get base price
        cur.execute("SELECT basePrice FROM city WHERE cityID = ?", (cityID,))
        base_price_row = cur.fetchone()
        if not base_price_row:
            conn.close()
            raise ValueError("City not found")
        base_price = base_price_row[0]

        # Start booking ID
        cur.execute("SELECT MAX(bookingID) FROM booking")
        result = cur.fetchone()
        next_booking_id = 1 if result[0] is None else result[0] + 1

        successful_inserts = 0

        for seat_id in seatIDs:
            # Check if seat already booked
            cur.execute("SELECT 1 FROM booking WHERE showID = ? AND seatID = ? AND cancelled = 0", (showID, seat_id))
            if cur.fetchone():
                print(f"Seat {seat_id} is already booked. Skipping.")
                continue

            # Get seat type
            cur.execute("SELECT seatType FROM seat WHERE seatID = ? AND screenID = ?", (seat_id, screenID))
            seat_row = cur.fetchone()
            if not seat_row:
                print(f"Seat {seat_id} not found on screen {screenID}")
                continue

            seat_type = seat_row[0]

            # Calculate price
            if seat_type.lower() == "lower":
                price = base_price
            elif seat_type.lower() == "upper":
                price = base_price * 1.2
            elif seat_type.lower() == "vip":
                price = base_price * 1.44
            else:
                price = base_price

            cur.execute('''
                INSERT INTO booking (bookingID, showID, seatID, price, staffID)
                VALUES (?, ?, ?, ?, ?)
            ''', (next_booking_id, showID, seat_id, price, staffID))
            next_booking_id += 1
            successful_inserts += 1

        if successful_inserts > 0:
            conn.commit()
            messagebox.showinfo("Success", "Booking added successfully.")
        else:
            messagebox.showwarning("Notice", "No seats were booked. They may already be taken.")

        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to add booking: {str(e)}")
