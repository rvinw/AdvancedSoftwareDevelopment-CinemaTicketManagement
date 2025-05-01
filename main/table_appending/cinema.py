# 23035803
# Written By Arvin Valad Khani

import sqlite3
import random

def setup_cinemas_and_screens():
    con = sqlite3.connect("HorizonCinema.db")
    cur = con.cursor()

    cities = ["Birmingham", "Bristol", "Cardiff", "London"]
    screen_capacities = [120, 100, 80, 70, 60, 50]

    for city in cities:
        # Fetch cityID
        cur.execute("SELECT cityID FROM city WHERE cityName = ?", (city,))
        result = cur.fetchone()
        if not result:
            print(f"City '{city}' not found in database. Skipping.")
            continue
        city_id = result[0]

        for suffix in ["I", "II"]:
            cinema_name = f"{city} {suffix}"
            num_screens = random.randint(2, 6)  # Or fix this to a specific number

            # Insert cinema with numberOfScreens
            cur.execute('''
                INSERT INTO cinema (cinemaName, numberOfScreens, cityID)
                VALUES (?, ?, ?)
            ''', (cinema_name, num_screens, city_id))
            cinema_id = cur.lastrowid

            print(f"Inserted {cinema_name} with {num_screens} screens.")

            # Insert screens with corresponding capacities
            for screen_num in range(1, num_screens + 1):
                capacity = screen_capacities[screen_num - 1]  # Pick from fixed list
                cur.execute('''
                    INSERT INTO screen (cinemaID, screenName, capacity)
                    VALUES (?, ?, ?)
                ''', (cinema_id, screen_num, capacity))

    con.commit()
    con.close()
    print("All cinemas and screens added.")
    
setup_cinemas_and_screens()