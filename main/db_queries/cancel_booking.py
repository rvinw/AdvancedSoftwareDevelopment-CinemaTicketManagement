import sqlite3
from tkinter import messagebox
from datetime import datetime, timedelta

def cancel_booking(bookingID):
    try:
        conn = sqlite3.connect("HorizonCinema.db")
        cur = conn.cursor()

        # Check if booking exists and isn't already cancelled
        cur.execute("SELECT showID FROM booking WHERE bookingID = ? AND cancelled = 0", (bookingID,))
        row = cur.fetchone()
        if not row:
            messagebox.showerror("Error", f"No active booking found with ID {bookingID}.")
            conn.close()
            return

        showID = row[0]

        # Get show date
        cur.execute("SELECT showDateTime FROM show WHERE showID = ?", (showID,))
        show_row = cur.fetchone()
        if not show_row:
            messagebox.showerror("Error", "Show for this booking no longer exists.")
            conn.close()
            return

        show_datetime = datetime.strptime(show_row[0], "%Y-%m-%d %H:%M:%S")
        now = datetime.now()

        # Must be at least 1 day before the show
        if now > show_datetime - timedelta(days=1):
            messagebox.showerror("Error", "Booking can only be cancelled at least 1 day before the show.")
            conn.close()
            return

        # Calculate total refund
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