# Written By Arvin Valad Khani (23035803)


import sqlite3
import math

def add_seat(seatID, seatType, screenID):
    con = sqlite3.connect("HorizonCinema.db")
    cur = con.cursor()

    cur.execute('''
        INSERT INTO seat (seatID, seatType, screenID)
        VALUES (?, ?, ?)
    ''', (seatID, seatType, screenID))

    con.commit()
    con.close()

# Seat distributions per screen (48 screens)
# You can adjust these manually or generate them dynamically
screen_seat_counts = [
    60, 70, 85, 95, 105, 120,  # Example: 6 screens for cinema 1
    60, 70, 85, 95, 105, 120,  # cinema 2
    60, 70, 85, 95, 105, 120,  # cinema 3
    60, 70, 85, 95, 105, 120,  # cinema 4
    60, 70, 85, 95, 105, 120,  # cinema 5
    60, 70, 85, 95, 105, 120,  # cinema 6
    60, 70, 85, 95, 105, 120,  # cinema 7
    60, 70, 85, 95, 105, 120   # cinema 8
]

screenID = 1

for seat_count in screen_seat_counts:
    lower_count = int(seat_count * 0.3)
    vip_count = min(10, int(seat_count * 0.1))
    upper_count = seat_count - lower_count - vip_count

    seatID = 1

    for _ in range(lower_count):
        add_seat(seatID, "lower", screenID)
        seatID += 1

    for _ in range(upper_count):
        add_seat(seatID, "upper", screenID)
        seatID += 1

    for _ in range(vip_count):
        add_seat(seatID, "vip", screenID)
        seatID += 1

    print(f"Screen {screenID}: {seat_count} seats added.")
    screenID += 1