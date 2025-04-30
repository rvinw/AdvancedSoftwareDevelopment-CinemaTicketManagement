import sqlite3

def get_movies():
    try:
        conn = sqlite3.connect("HorizonCinema.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT title, description, genre, age, rating, runTime, directors, "cast"
            FROM movie
        """)

        movies = cursor.fetchall()
        conn.close()

        movie_list = []
        for movie in movies:
            movie_dict = {
                "title": movie[0],
                "description": movie[1],
                "genre": movie[2],
                "age": movie[3],
                "rating": movie[4],
                "runTime": movie[5],
                "directors": movie[6],
                "cast": movie[7],
            }
            movie_list.append(movie_dict)

        return movie_list

    except sqlite3.Error as e:
        print(f"Error fetching movies from the database: {e}")
        return []
    

import sqlite3

def get_title():
    conn = sqlite3.connect("HorizonCinema.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT title
        FROM movie
    """)
    
    results = cursor.fetchall()
    conn.close()

    # Extract titles from list of tuples
    titles = [row[0] for row in results]
    return titles

def get_cinema_name():
    conn = sqlite3.connect("HorizonCinema.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT cinemaName
        FROM cinema
    """)
    
    results = cursor.fetchall()
    conn.close()

    # Extract titles from list of tuples
    cinema = [row[0] for row in results]
    return cinema

def get_show_id(movie_title, cinema_name, show_date):
    conn = sqlite3.connect("HorizonCinema.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT s.showID FROM show s
        JOIN movie m ON s.movieID = m.movieID
        JOIN cinema c ON s.cinemaID = c.cinemaID
        WHERE m.title = ? AND c.cinemaName = ? AND DATE(s.showDateTime) = ?
    """, (movie_title, cinema_name, show_date))
    row = cur.fetchone()
    conn.close()
    if row:
        return row[0]
    raise ValueError("No matching show found.")

# Pricing per seat type
SEAT_PRICES = {
    "lower": 7.00,
    "upper": 9.00,
    "vip": 12.00
}