# Written By Arvin Valad Khani (23035803)

import sqlite3
from tkinter import messagebox


def get_booking_info(bookingID):
    
    try:
        conn = sqlite3.connect("HorizonCinema.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM booking WHERE bookingID = ?", (bookingID,))
        row = cur.fetchone()
        conn.close()
        return row
    except Exception as e:
        return f"Error: {str(e)}"

def cancel_booking(bookingID):
    try:
        conn = sqlite3.connect("HorizonCinema.db")
        cur = conn.cursor()

        # Check booking exists and isn't cancelled
        cur.execute("SELECT * FROM booking WHERE bookingID = ? AND cancelled = 0", (bookingID,))
        row = cur.fetchone()
        if not row:
            messagebox.showerror("Error", f"No active booking found with ID {bookingID}.")
            conn.close()
            return

        # Refund (optional — if you care about refund amount)
        cur.execute("SELECT SUM(price) FROM booking WHERE bookingID = ?", (bookingID,))
        refund_row = cur.fetchone()
        refund_amount = refund_row[0] if refund_row and refund_row[0] else 0.0

        # Mark as cancelled
        cur.execute("UPDATE booking SET cancelled = 1 WHERE bookingID = ?", (bookingID,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Booking Cancelled", f"Booking #{bookingID} cancelled.\nRefund Amount: £{refund_amount:.2f}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to cancel booking: {str(e)}")

def uncancel_booking(bookingID):
    try:
        conn = sqlite3.connect("HorizonCinema.db")
        cur = conn.cursor()

        # Check if booking exists and is cancelled
        cur.execute("SELECT * FROM booking WHERE bookingID = ? AND cancelled = 1", (bookingID,))
        row = cur.fetchone()
        if not row:
                return False, f"No cancelled booking found with ID {bookingID}."

        # Update to uncancel
        cur.execute("UPDATE booking SET cancelled = 0 WHERE bookingID = ?", (bookingID,))
        conn.commit()
        conn.close()

        return True, f"Booking #{bookingID} has been restored."

    except Exception as e:
        return False, f"Database error: {str(e)}"