#!/usr/bin/env python
import datetime
import psycopg2
import sys
import timeit

def q1():
  '''
  What movies share at least one actor?
  '''
  query = '''
    SELECT m1.doc->'title', m2.doc->'title'
    FROM movies m1
    JOIN movies m2 ON ((m1.doc->>'release_date')::date - (m2.doc->>'release_date')::date) >= 365*5
    WHERE (
      SELECT COUNT(*) FROM (
        SELECT jsonb_array_elements(m1.doc->'actors')
        INTERSECT
        SELECT jsonb_array_elements(m2.doc->'actors')
      ) actors_intersection
    ) >= 1
  '''
  return query

def q2():
  '''
  What movies are in both the "action" and "adventure" genres?
  '''
  query = '''
    SELECT
      m.title
    FROM
      movies m
    JOIN
      movies_genres mg
    ON
      mg.movie_id = m.id AND
      mg.genre IN ('Action', 'Adventure')
    GROUP BY
      m.id,
      m.title
    HAVING
      COUNT(DISTINCT mg.genre) = 2
  '''
  return query

def q3():
  '''
  What movies have at least half of their reviewers from Canada? Exclude
  movies with no reviews.
  '''
  query = '''
    SELECT
      m.title
    FROM
      movies m,
      reviews r1,
      reviews r2
    WHERE
      m.id = r1.movie_id AND
      m.id = r2.movie_id AND
      r2.user_country = 'CA'
    GROUP BY
      m.id, m.title
    HAVING
      (COUNT(DISTINCT r2.id)::float / COUNT(DISTINCT r1.id)) >= 0.5
  '''
  return query

def q4():
  '''
  What movies were released in the last year?
  '''
  time_threshold = datetime.datetime.now()
  time_threshold = time_threshold.replace(year = time_threshold.year - 1)
  strtime = time_threshold.strftime('%Y-%m-%d')

  query = '''
    SELECT m.title
    FROM movies m
    WHERE m.release_date >= '%s'
  ''' % strtime
  return query

def q5():
  '''
  What is the average rating of each movie?
  '''
  query = '''
    SELECT
      m.title,
      AVG(r.rating)
    FROM
      movies m
    JOIN
      reviews r ON r.movie_id = m.id
    GROUP BY
      m.id, m.title
  '''
  return query

def q6():
  '''
  What movies contained given actor?
  '''
  desired_actor_id = 3
  query = '''
    SELECT
      m.title
    FROM
      movies m,
      actors a,
      movies_actors ma
    WHERE
      ma.movie_id = m.id AND
      ma.actor_id = a.id AND
      ma.actor_id = %s
  ''' % desired_actor_id
  return query

def run_query(conn, query):
  cur = conn.cursor()
  cur.execute(query)
  print(cur.fetchall())
  conn.commit()
  cur.close()
  
def main():
  conn = psycopg2.connect("dbname=movies_relational user=postgres")

  for gen_query in (q2, q3, q4, q5, q6):
    timer = timeit.Timer(setup='gc.enable()', stmt=lambda: run_query(conn, gen_query()))
    print((gen_query, timer.repeat(repeat=1, number=1)), file=sys.stderr)

  conn.close()

main()
