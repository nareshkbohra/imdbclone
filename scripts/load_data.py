import json
import sqlite3

with open("imdb.json") as fd:
    data = json.load(fd)


movies = []
genres = set()

for m in data:
    for genre in m["genre"]:
        genres.add(genre)

    movies.append((m["name"], m["director"], m["imdb_score"], m["99popularity"]))

genres = [(genre.strip(),) for genre in genres]

con = sqlite3.connect("db.sqlite")

con.execute("delete from movies;")
con.execute("delete from genre;")
con.execute("delete from movie_genre;")
con.commit()

con.executemany(
    "insert into movies(name, director, imdb_score, popularity) values (?,?,?,?)",
    movies,
)

con.executemany("insert into genre(name) values (?)", genres)

con.commit()


result = con.execute("select id, name, director from movies;")
movies = result.fetchall()
movie_id_map = {(name, director): mid for mid, name, director in movies}

result = con.execute("select id, name from genre;")
genres = result.fetchall()
genre_id_map = {name: gid for gid, name in genres}

movie_genre_entries = []

for movie in data:
    key = (movie["name"], movie["director"])
    movie_id = movie_id_map[key]

    for genre in movie["genre"]:
        genre_id = genre_id_map[genre.strip()]
        movie_genre_entries.append((movie_id, genre_id))

con.executemany(
    "insert into movie_genre(movie_id, genre_id) values (?, ?)", movie_genre_entries
)

con.commit()
