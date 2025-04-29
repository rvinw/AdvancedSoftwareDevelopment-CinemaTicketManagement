import sqlite3

def add_booking(showID, seatIDs):
    conn = sqlite3.connect("HorizonCinema.db")
    cur = conn.cursor()

    # Get next booking ID by checking the current max
    cur.execute("SELECT MAX(bookingID) FROM booking")
    result = cur.fetchone()
    next_booking_id = 1 if result[0] is None else result[0] + 1

    for seat_id in seatIDs:
        # === Placeholder for price calculation logic ===
        # Example:
        # price = calculate_price(seat_id, showID)
        price = 10.0  # Temporary fixed value

        cur.execute('''
            INSERT INTO booking (bookingID, showID, seatID, price)
            VALUES (?, ?, ?, ?)
        ''', (next_booking_id, showID, seat_id, price))

    conn.commit()
    conn.close()
    
    add_booking()