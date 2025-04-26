import sqlite3

def add_movie(title, description, genre, age, rating, director, cast):
    con = sqlite3.connect("HorizonCinema.db")
    cur = con.cursor()

    cur.execute('''
    INSERT INTO movie (title, description, genre, age, rating, director, cast)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (title, description, genre, age, rating, director, cast))

    con.commit()
    con.close()
    
title = ''
description = ''
genre = ''
age = ''
rating = ''
director = ''
cast = ''

add_movie(title, description, genre, age, rating, director, cast)