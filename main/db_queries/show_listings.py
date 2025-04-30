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