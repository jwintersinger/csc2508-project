#!/usr/bin/env python
import json
import sys
import random
import math
import string

class DocGenerator:
  def __init__(self, total_movies):
    self._total_movies = total_movies
    self._current_movie_id = 0
    self._current_actor_id = 0
    self._current_review_id = 0
    self._actors = []

  def _generate_str(self, lower_limit, upper_limit):
    length = random.randrange(lower_limit, upper_limit + 1)
    chars = string.ascii_uppercase + string.digits
    title = ''.join(random.choice(chars) for _ in range(length))
    return title

  def _generate_date(self):
    year = random.randrange(1900, 2015)
    month = random.randrange(1, 13)
    day = random.randrange(1, 29)
    return '%.4d-%.2d-%.2d' % (year, month, day)

  def _generate_genres(self):
    genres = [
      'Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama',
      'Family', 'Fantasy', 'Film-Noir', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance',
      'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western'
    ]
    num_genres = random.randrange(1, 4)
    return sorted(random.sample(genres, num_genres))

  def _generate_name(self):
    return ' '.join([self._generate_str(4, 12), self._generate_str(6, 20)])

  def _generate_movie_list(self):
    mu, sigma = 5, 2
    num_movies = abs(round(random.gauss(mu, sigma)))
    all_movie_ids = range(1, self._total_movies + 1)

    if num_movies > len(all_movie_ids):
      num_movies = len(all_movie_ids)
    movie_list = sorted(random.sample(all_movie_ids, num_movies))
    return movie_list

  def _generate_actor(self, movie_id):
    self._current_actor_id += 1
    other_movies = [mid for mid in self._generate_movie_list() if mid != movie_id]
    actor = {
      'id': self._current_actor_id,
      'name': self._generate_name(),
      'birth_date': self._generate_date(),
      'movies': other_movies,
    }
    return actor

  def _generate_country(self):
    if random.random() < 0.25:
      return 'CA'
    else:
      europe = ['AT', 'BE', 'BG', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IE', 'IT',
        'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE', 'GB',]
      namerica = ['CA', 'US']
      return random.choice(europe + namerica)

  def _generate_review_text(self):
    mu, sigma = 20, 5
    word_count = abs(round(random.gauss(mu, sigma)))
    return ' '.join([self._generate_str(3, 20) for _ in range(word_count)])
    
  def _generate_review(self):
    self._current_review_id += 1
    rating = random.randrange(1, 6)
    review = {
      'id': self._current_review_id,
      'rating': rating,
      'name': self._generate_name(),
      'country': self._generate_country(),
      'recent_purchases': self._generate_movie_list(),
      'text': self._generate_review_text(),
    }
    return review

  def _generate_movie(self):
    self._current_movie_id += 1
    num_actors = abs(round(random.gauss(20, 8)))
    num_reviews = abs(round(random.gauss(15, 6)))

    doc = {
      "id": self._current_movie_id,
      "title": self._generate_str(6, 28),
      "release_date": self._generate_date(),
      "genre": self._generate_genres(),
      "actors": [self._generate_actor(self._current_movie_id) for _ in range(num_actors)],
      "reviews": [self._generate_review() for _ in range(num_reviews)],
    }
    return doc

  def generate(self):
    for _ in range(self._total_movies):
      yield self._generate_movie()

def main():
  movie_count = int(sys.argv[1])
  gen = DocGenerator(movie_count)
  for movie in gen.generate():
    print(json.dumps(movie))

main()
