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
    SELECT m.doc->'title'
    FROM movies m
    WHERE m.doc->>'release_date' >= '%s'
  ''' % strtime
  return query

def q2():
  '''
  What movies are in both the "action" and "adventure" genres?
  '''
  query = '''
    SELECT m.doc->'title' FROM movies m
    WHERE m.doc->'genre' ?& array['Action', 'Adventure']
  '''
  return query

def q3():
  '''
  What is the average rating of each movie?
  '''
  query = '''
    SELECT
      m.doc->'title',
      AVG((r->>'rating')::int)
    FROM
      movies m,
      jsonb_array_elements(m.doc->'reviews') r
    GROUP BY
      m.doc->'id',
      m.doc->'title'
  '''
  return query

def q4():
  '''
  What movies contained given actor?
  '''
  desired_actor_id = 3
  query = '''
    SELECT
      m.doc->'title'
    FROM
      movies m,
      jsonb_array_elements(m.doc->'actors') a
    WHERE
      (a->>'id')::int = %s
    GROUP BY
      m.doc->'id',
      m.doc->'title'
  ''' % desired_actor_id
  return query

def q5():
  '''
  What movies have at least half of their reviewers from Canada? Exclude
  movies with no reviews.
  '''
  query = '''
    SELECT
      m1.doc->'id' mid,
      m1.doc->'title' mtitle,
      jsonb_array_length(m1.doc->'reviews') as total_reviews,
      COUNT(desired_reviews.*) as num_desired_reviews
    FROM
      movies m1,
      jsonb_array_elements(m1.doc->'reviews') desired_reviews
    WHERE
      (desired_reviews->'user'->>'country') = 'CA'
    GROUP BY
      mid, mtitle, total_reviews
    HAVING
      (COUNT(desired_reviews.*)::float / jsonb_array_length(m1.doc->'reviews')) >= 0.5
  '''
  return query

def q6():
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

def run_query(conn, query):
  cur = conn.cursor()
  cur.execute(query)
  print(cur.fetchall())
  conn.commit()
  cur.close()
  
def main():
  db_name = sys.argv[1]
  conn = psycopg2.connect("dbname=%s user=postgres" % db_name)

  #for gen_query in (q1, q2, q3, q4, q5):
  for gen_query in (q6,):
    timer = timeit.Timer(setup='gc.enable()', stmt=lambda: run_query(conn, gen_query()))
    results = timer.repeat(repeat=10, number=1)
    for result in results:
      print('%s,%s' % (gen_query.__name__, result), file=sys.stderr)
      sys.stderr.flush()

  conn.close()

main()
