# Written By Arvin Valad Khani (23035803)

import sqlite3

def add_movie_func(title, description, genre, age, rating, runtime, directors, cast):
    con = sqlite3.connect("HorizonCinema.db")
    cur = con.cursor()

    cur.execute('''
        INSERT INTO movie (title, description, genre, age, rating, runTime, directors, cast)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title, description, genre, age, rating, runtime, directors, cast))

    con.commit()
    con.close()
    
    return


# Sample movie data structured for insertion
movies = [
    {
        "title": "A Minecraft Movie",
        "description": "Four misfits — Garrett “The Garbage Man” Garrison (Jason Momoa), Henry (Sebastian Eugene Hansen), Natalie (Emma Myers) and Dawn (Danielle Brooks)—find themselves struggling with ordinary problems when they are suddenly pulled through a mysterious portal into the Overworld: a bizarre, cubic wonderland that thrives on imagination. To get back home, they’ll have to master this world (and protect it from evil things like Piglins and Zombies, too) while embarking on a magical quest with an unexpected, expert crafter, Steve (Jack Black).",
        "genre": "Action",
        "age": "PG",
        "rating": 5.9,
        "runTime": "101mins",
        "directors": "Jared Hess",
        "cast": "Jason Momoa, Jack Black, Emma Myers, Jennifer Coolidge, Danielle Brooks, Sebastian Eugene Hansen, Kate McKinnon, Jemaine Clement"
    },
    {
        "title": "AVATAR",
        "description": "When his brother is killed in a robbery, paraplegic Marine Jake Sully decides to take his place in a mission on the distant world of Pandora. There he learns of greedy corporate figurehead Parker Selfridge's intentions of driving off the native humanoid \"Na'vi\" in order to mine for the precious material scattered throughout their rich woodland...",
        "genre": "Action",
        "age": "12A",
        "rating": 7.9,
        "runTime": "162mins",
        "directors": "James Cameron",
        "cast": "Sam Worthington, Zoe Saldana, Sigourney Weaver"
    },
    {
        "title": "INSIDE OUT 2",
        "description": "Now a teenager, Riley is dealing with all-new emotions as she starts high school. Joy, Sadness, Anger, Fear, and Disgust are thrown for a loop when a surprise visitor arrives in Headquarters: Anxiety...",
        "genre": "Coming-Of-Age",
        "age": "U",
        "rating": 7.5,
        "runTime": "96mins",
        "directors": "Kelsey Mann",
        "cast": "Amy Poehler, Phyllis Smith, Lewis Black, Tony Hale, Maya Hawke, Ayo Edebiri"
    },
    {
        "title": "OPPENHEIMER",
        "description": "A brilliant theoretical physicist, J. Robert Oppenheimer, is recruited to lead the Manhattan Project—the secret operation that developed the first nuclear weapons...",
        "genre": "Docudrama",
        "age": "15",
        "rating": 8.3,
        "runTime": "180mins",
        "directors": "Christopher Nolan",
        "cast": "Cillian Murphy, Emily Blunt, Matt Damon, Robert Downey Jr., Florence Pugh, Rami Malek"
    },
    {
        "title": "THE SUPER MARIO BROS. MOVIE",
        "description": "A Brooklyn plumber named Mario travels through a mysterious pipe and lands in a magical new world. When Bowser threatens the peace of the Mushroom Kingdom...",
        "genre": "Action",
        "age": "PG",
        "rating": 7.0,
        "runTime": "92mins",
        "directors": "Aaron Horvath, Michael Jelenic",
        "cast": "Chris Pratt, Anya Taylor-Joy, Charlie Day, Jack Black, Keegan-Michael Key, Seth Rogen"
    },
    {
        "title": "DUNE: PART TWO",
        "description": "Paul Atreides unites with the Fremen of Arrakis as he prepares to strike back against House Harkonnen...",
        "genre": "Action",
        "age": "12A",
        "rating": 8.5,
        "runTime": "166mins",
        "directors": "Denis Villeneuve",
        "cast": "Timothée Chalamet, Zendaya, Rebecca Ferguson, Austin Butler, Florence Pugh, Javier Bardem"
    },
    {
        "title": "SPIDER-MAN: ACROSS THE SPIDER-VERSE",
        "description": "Miles Morales returns for another web-slinging adventure through the multiverse. When he meets a team of Spider-People trying to protect the fabric of reality...",
        "genre": "Superhero",
        "age": "PG",
        "rating": 8.5,
        "runTime": "140mins",
        "directors": "Joaquim Dos Santos, Kemp Powers, Justin K. Thompson",
        "cast": "Shameik Moore, Hailee Steinfeld, Oscar Isaac, Daniel Kaluuya, Issa Rae"
    },
    {
        "title": "BARBIE",
        "description": "Living in the perfect world of Barbie Land, Barbie starts to question her place in the universe and ventures into the Real World with Ken by her side...",
        "genre": "Comedy",
        "age": "12",
        "rating": 6.8,
        "runTime": "114mins",
        "directors": "Greta Gerwig",
        "cast": "Margot Robbie, Ryan Gosling, America Ferrera, Kate McKinnon, Simu Liu, Will Ferrell"
    },
    {
        "title": "WONKA",
        "description": "Before the chocolate factory, there was a dream. A young Willy Wonka sets off to make a name for himself in a world that doesn’t believe in magic...",
        "genre": "Fantasy",
        "age": "PG",
        "rating": 7.0,
        "runTime": "114mins",
        "directors": "Paul King",
        "cast": "Timothée Chalamet, Olivia Colman, Keegan-Michael Key, Rowan Atkinson, Hugh Grant"
    },
    {
        "title": "GODZILLA X KONG: THE NEW EMPIRE",
        "description": "The epic battle continues as Godzilla and Kong face off once more—but a new threat emerges from deep within the Hollow Earth...",
        "genre": "Action",
        "age": "12A",
        "rating": 6.0,
        "runTime": "115mins",
        "directors": "Adam Wingard",
        "cast": "Rebecca Hall, Brian Tyree Henry, Dan Stevens, Kaylee Hottle"
    }
]

# Insert into database
con = sqlite3.connect("HorizonCinema.db")
cur = con.cursor()



for movie in movies:
    cur.execute('''
    INSERT OR IGNORE INTO movie (title, description, genre, age, rating, runTime, directors, cast)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        movie["title"],
        movie["description"],
        movie["genre"],
        movie["age"],
        movie["rating"],
        movie["runTime"],
        movie["directors"],
        movie["cast"]
    ))

con.commit()
con.close()
