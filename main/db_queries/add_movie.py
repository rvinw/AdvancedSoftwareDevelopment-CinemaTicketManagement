import sqlite3

def add_movie(title, description, genre, age, rating, director, cast):
    con = sqlite3.connect("HorizonCinema.db")
    cur = con.cursor()

    cur.execute('''
    INSERT INTO movie (title, description, genre, age, rating, directors, cast)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (title, description, genre, age, rating, director, cast))

    con.commit()
    con.close()
    
title = 'Oppenheimer'
description = "A brilliant theoretical physicist, J. Robert Oppenheimer, is recruited to lead the Manhattan Project—the secret operation that developed the first nuclear weapons..."
genre = 'Thriller/Historical Drama'
age = 'R'
rating = 8.3
director = 'Christopher Nolan'
cast = 'Cillian Murphy, Emily Blunt, Matt Damon, Robert Downey Jr., Florence Pugh, Rami Malek'

add_movie(title, description, genre, age, rating, director, cast)