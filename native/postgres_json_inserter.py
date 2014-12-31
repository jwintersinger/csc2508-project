#!/usr/bin/env python
import psycopg2
import sys

def main():
  conn = psycopg2.connect("dbname=movies_json user=postgres")
  cur = conn.cursor()

  cur.execute('DROP TABLE IF EXISTS movies')
  cur.execute('CREATE TABLE movies (doc JSONB)')

  for line in sys.stdin:
    cur.execute('INSERT INTO movies (doc) VALUES (%s)', (line,))

  conn.commit()
  cur.close()
  conn.close()

main()
