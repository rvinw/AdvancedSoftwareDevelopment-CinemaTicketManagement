import sqlite3
from datetime import datetime, timedelta
from tkinter import messagebox

# Function 1: Get Seat Matrix for a given showID
def get_seat_matrix(showID):
    try:
        conn = sqlite3.connect("HorizonCinema.db")
        cur = conn.cursor()

        # Step 1: Get screenID from the showID
        cur.execute("SELECT screenID FROM show WHERE showID = ?", (showID,))
        row = cur.fetchone()
        if not row:
            raise ValueError("Invalid showID provided.")
        screenID = row[0]

        # Step 2: Get screen capacity (for organizing rows)
        cur.execute("SELECT capacity FROM screen WHERE screenID = ?", (screenID,))
        cap_row = cur.fetchone()
        if not cap_row:
            raise ValueError("Screen not found.")
        capacity = cap_row[0]

        # Step 3: Get all seat info for this screen
        cur.execute("SELECT seatID, seatType FROM seat WHERE screenID = ? ORDER BY seatID", (screenID,))
        seats = cur.fetchall()

        # Step 4: Get booked seatIDs for this show (excluding cancelled)
        cur.execute("""
            SELECT seatID FROM booking 
            WHERE showID = ? AND cancelled = 0
        """, (showID,))
        booked_seats = set(row[0] for row in cur.fetchall())

        # Step 5: Build seat matrix with availability
        seat_matrix = []
        row = []
        for idx, (seatID, seatType) in enumerate(seats):
            available = seatID not in booked_seats
            row.append([seatID, seatType, available])
            if (idx + 1) % 10 == 0 or (idx + 1) == capacity:
                seat_matrix.append(row)
                row = []

        if row:  # any remaining seats in last row
            seat_matrix.append(row)

        conn.close()
        return seat_matrix

    except Exception as e:
        print(f"Error retrieving seat matrix: {e}")
        return []

# Function 2: Cancel booking based on bookingID
def cancel_booking(bookingID):
    try:
        conn = sqlite3.connect("HorizonCinema.db")
        cur = conn.cursor()

        # Step 1: Get booking details
        cur.execute("SELECT showID, seatID FROM booking WHERE bookingID = ? AND cancelled = 0", (bookingID,))
        booking = cur.fetchone()
        if not booking:
            messagebox.showerror("Error", "Booking not found or already cancelled.")
            conn.close()
            return

        showID, seatID = booking

        # Step 2: Get show datetime
        cur.execute("SELECT showDateTime FROM show WHERE showID = ?", (showID,))
        show_row = cur.fetchone()
        if not show_row:
            messagebox.showerror("Error", "Invalid showID.")
            conn.close()
            return
        show_datetime = datetime.strptime(show_row[0], "%Y-%m-%d %H:%M:%S")
        now = datetime.now()

        # Step 3: Check if cancellation is allowed (at least 1 day prior to show)
        if show_datetime <= now + timedelta(days=1):
            messagebox.showerror("Error", "Cannot cancel booking within 24 hours of the show.")
            conn.close()
            return

        # Step 4: Calculate the refund price (same as the booked price)
        cur.execute("SELECT price FROM booking WHERE bookingID = ?", (bookingID,))
        price_row = cur.fetchone()
        if not price_row:
            messagebox.showerror("Error", "Booking price not found.")
            conn.close()
            return
        price = price_row[0]

        # Step 5: Update booking to cancelled
        cur.execute("UPDATE booking SET cancelled = 1 WHERE bookingID = ?", (bookingID,))
        
        # Step 6: Commit changes and notify user
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Booking cancelled. Refund: £{price:.2f}")
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to cancel booking: {str(e)}")