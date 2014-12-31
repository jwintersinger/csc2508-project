#!/usr/bin/env python3
import datetime
import psycopg2
import sys
import timeit

def q1():
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

def q4():
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

def q5():
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

def q6():
  '''
  What movies share at least one actor?
  '''
  query = '''
    SELECT m1.title, m2.title
    FROM movies m1
    JOIN movies m2 ON m1.release_date::date - m2.release_date::date >= 365*5
    WHERE (
      SELECT COUNT(*) FROM (
        SELECT ma1.actor_id FROM movies_actors ma1 WHERE ma1.movie_id = m1.id
        INTERSECT
        SELECT ma2.actor_id FROM movies_actors ma2 WHERE ma2.movie_id = m2.id
      ) actors_intersection
    ) >= 1
  '''
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
    results = timer.repeat(repeat=10, number=1)
    for result in results:
      print('%s,%s' % (gen_query.__name__, result), file=sys.stderr)

  conn.close()

main()
