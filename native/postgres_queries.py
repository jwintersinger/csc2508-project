#!/usr/bin/env python
import datetime
import psycopg2

def q1():
  '''
  What movies share at least one actor?
  '''
  query = '''
    SELECT m1.doc->'title', m2.doc->'title'
    FROM movies m1
    JOIN movies m2 ON (m1.doc->'id') > (m2.doc->'id')
    WHERE (
      SELECT COUNT(*) FROM (
        SELECT jsonb_array_elements(m1.doc->'actors')
        INTERSECT
        SELECT jsonb_array_elements(m2.doc->'actors')
      ) actors_intersection
    ) >= 1
    AND ABS((m1.doc->>'release_date')::date - (m2.doc->>'release_date')::date) > 365*5;
  '''
  return query

def q2():
  '''
  What movies are in both the "action" and "adventure" genres?
  '''
  query = '''
    SELECT m.doc->'title' FROM movies m
    WHERE m.doc->'genre' ?& array['Action', 'Adventure'];
  '''
  return query

def q3():
  '''
  What movies have at least half of their reviewers from Canada? Exclude
  movies with no reviews.
  '''
  query = '''
    SELECT
      m1.doc->'id' mid,
      m1.doc->'title' mtitle,
      jsonb_array_length(m1.doc->'reviews') as total_reviews,
      COUNT(desired_reviews.*) as desired_reviews
    FROM
      movies m1,
      jsonb_array_elements(m1.doc->'reviews') desired_reviews
    WHERE (desired_reviews->'user'->>'country') = 'CA'
    GROUP BY mid, mtitle, total_reviews;
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
    SELECT m.doc->'title'
    FROM movies m
    WHERE m.doc->>'release_date' >= '%s'
  ''' % strtime
  return query
  
def main():
  conn = psycopg2.connect("dbname=postgres user=postgres")
  cur = conn.cursor()

  for gen_query in (q1, q2, q3, q4):
    query = gen_query()
    cur.execute(query)
    print(cur.fetchall())

  conn.commit()
  cur.close()
  conn.close()

main()
