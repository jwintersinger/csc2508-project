import pymongo
import datetime

def q1(col):
  def _do_movies_share_actors(m1, m2, threshold):
    sorter = lambda a: a['id']
    m1['actors'].sort(key = sorter)
    m2['actors'].sort(key = sorter)

    last_a1 = None
    last_a2 = None
    shared_actors = 0

    for a1 in m1['actors']:
      a1_id = a1['id']
      if a1_id == last_a1:
        continue
      last_a1 = a1_id

      for a2 in m2['actors']:
        a2_id = a2['id']
        if a2_id == last_a2:
          continue
        last_a2 = a2_id

        if a1_id == a2_id:
          shared_actors += 1
          if shared_actors >= threshold:
            return True
    return False

  def _add_movies_with_shared_actors(movie):
    movie['movies_with_shared_actors'] = []
    others = col.find({'_id': {'$gt': movie['_id']}})

    for other in others:
      if _do_movies_share_actors(movie, other, 1):
        movie['movies_with_shared_actors'].append(other)
    return movie

  movies = map(_add_movies_with_shared_actors, col.find())
  movies = [m for m in movies if len(m['movies_with_shared_actors']) > 0]
  for movie in movies:
    print((movie['title'], [m['title'] for m in movie['movies_with_shared_actors']]))

def q2(col):
  movies = col.find({'genre': {'$all': ['Action', 'Adventure']}})
  for movie in movies:
    print(movie['title'])

def q3(col):
  target_country = 'CA'
  target_threshold = 0
  
  agg = col.aggregate([
    {'$unwind': '$reviews'},
    {'$project': {
      '_id': False,
      'movie_id': '$title',
      'in_target_country': {
        '$cond': {
          'if': {'$eq': ['$reviews.user.country', target_country] },
          'then': 1,
          'else': -1
        }
      }
    }},
    {'$group': {
      '_id': '$movie_id',
      'review_country_sum': { '$sum': '$in_target_country' }
    }},
    {'$match': {'review_country_sum': {'$gte': target_threshold}}}
  ])
  for movie in agg['result']:
    print(movie)

def q4(col):
  time_threshold = datetime.datetime.now()
  time_threshold = time_threshold.replace(year = time_threshold.year - 1)
  strtime = time_threshold.strftime('%Y-%m-%d')
  movies = col.find({'release_date': {'$gte': strtime}})
  for movie in movies:
    print(movie['title'])

def main():
  client = pymongo.MongoClient('localhost', 27017)
  db = client.test
  col = db.lol

  q1(col)
  q2(col)
  q3(col)
  q4(col)

main()
