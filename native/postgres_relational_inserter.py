#!/usr/bin/env python3
import psycopg2
import sys
import json

def main():
  inserted_actors = set()

  db_name = sys.argv[1]
  conn = psycopg2.connect("dbname=%s user=postgres" % db_name)
  cur = conn.cursor()

  cur.execute('DROP TABLE IF EXISTS movies')
  cur.execute('DROP TABLE IF EXISTS actors')
  cur.execute('DROP TABLE IF EXISTS reviews')
  cur.execute('DROP TABLE IF EXISTS movies_actors')
  cur.execute('DROP TABLE IF EXISTS movies_genres')
  cur.execute('CREATE TABLE movies (id int, release_date char(10), title varchar(200))');
  cur.execute('CREATE TABLE actors (id int, birth_date char(10), name varchar(200))');
  cur.execute('CREATE TABLE reviews (id int, movie_id int, rating smallint, user_name varchar(200), user_country char(2), review text)');
  cur.execute('CREATE TABLE movies_actors (movie_id int, actor_id int)');
  cur.execute('CREATE TABLE movies_genres (movie_id int, genre varchar(50))');
  

  for line in sys.stdin:
    movie = json.loads(line)
    cur.execute('INSERT INTO movies (id, release_date, title) VALUES (%s, %s, %s)', (
      movie['id'],
      movie['release_date'],
      movie['title'],
    ))

    for genre in movie['genre']:
      cur.execute('INSERT INTO movies_genres (movie_id, genre) VALUES (%s, %s)', (
        movie['id'],
        genre,
      ))

    for actor in movie['actors']:
      if not actor['id'] in inserted_actors:
        inserted_actors.add(actor['id'])
        cur.execute('INSERT INTO actors (id, birth_date, name) VALUES (%s, %s, %s)', (
          actor['id'],
          actor['birth_date'],
          actor['name'],
        ))
      cur.execute('INSERT INTO movies_actors (movie_id, actor_id) VALUES (%s, %s)', (
        movie['id'],
        actor['id']
      ))
    
    for review in movie['reviews']:
      cur.execute('INSERT INTO reviews (id, movie_id, rating, user_name, user_country, review) VALUES (%s, %s, %s, %s, %s, %s)', (
        review['id'],
        movie['id'],
        review['rating'],
        review['user']['name'],
        review['user']['country'],
        review['text'],
      ))

  cur.execute('CREATE INDEX ON movies(id)')
  cur.execute('CREATE INDEX ON movies(title)')
  cur.execute('CREATE INDEX ON movies(release_date)')
  cur.execute('CREATE INDEX ON movies_genres(movie_id)')
  cur.execute('CREATE INDEX ON reviews(movie_id)')
  cur.execute('CREATE INDEX ON reviews(user_country)')
  cur.execute('CREATE INDEX ON actors(id)')
  cur.execute('CREATE INDEX ON movies_actors(movie_id)')
  cur.execute('CREATE INDEX ON movies_actors(actor_id)')

  conn.commit()
  cur.close()
  conn.close()

main()
