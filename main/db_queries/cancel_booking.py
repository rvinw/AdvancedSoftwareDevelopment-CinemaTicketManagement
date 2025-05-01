import sqlite3
from tkinter import messagebox
from datetime import datetime

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

        # Check booking exists and isn't already cancelled
        cur.execute("SELECT showID, price FROM booking WHERE bookingID = ? AND cancelled = 0", (bookingID,))
        booking = cur.fetchone()
        if not booking:
            messagebox.showerror("Error", f"No active booking found with ID {bookingID}.")
            conn.close()
            return

        showID, price = booking

        #Get showDateTime from 'show' table
        cur.execute("SELECT showDateTime FROM show WHERE showID = ?", (showID,))
        show_row = cur.fetchone()
        if not show_row:
            messagebox.showerror("Error", "Show information not found.")
            conn.close()
            return

        show_datetime = datetime.strptime(show_row[0], "%Y-%m-%d %H:%M")
        now = datetime.now()

        # Check if we are on the same day as the show and disallow cancellation on the same day
        if now.date() >= show_datetime.date():
            messagebox.showerror("Cancellation Not Allowed", "Tickets cannot be cancelled on the day of the show or after.")
            conn.close()
            return

        refund_amount = price * 0.5

    #Mark as cancelled
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