import datetime

def q1():
  '''
  What movies share at least one actor?
  '''
  query = '''
    SELECT m1.data->'title', m2.data->'title'
    FROM moviesj m1
    JOIN moviesj m2 ON (m1.data->'id') > (m2.data->'id')
    WHERE (
      SELECT COUNT(*) FROM (
        SELECT jsonb_array_elements(m1.data->'actors')
        INTERSECT
        SELECT jsonb_array_elements(m2.data->'actors')
      ) actors_intersection
    ) >= 1
    AND ABS((m1.data->>'release_date')::date - (m2.data->>'release_date')::date) > 365*5;
  '''

def q2():
  '''
  What movies are in both the "action" and "adventure" genres?
  '''
  query = '''
    SELECT m.doc->'title' FROM movies m
    WHERE m.doc->'genre' ?& array['Action', 'Adventure'];
  '''

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
    WHERE m1.doc->'release_date' >= '%s'
  ''' % strtime
  
def main():
  client = pymongo.MongoClient('localhost', 27017)
  db = client.test
  col = db.lol

  q1(col)
  q2(col)
  q3(col)
  q4(col)

main()
