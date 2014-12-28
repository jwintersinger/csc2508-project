import json
import psycopg2
import sys

def main():
  conn = psycopg2.connect("dbname=postgres user=postgres")
  cur = conn.cursor()

  cur.execute('DROP TABLE IF EXISTS movies')
  cur.execute('CREATE TABLE movies (doc JSONB)')
  #cur.execute('DELETE FROM movies');

  recs = json.load(sys.stdin)
  for rec in recs:
    json_str = json.dumps(rec)
    cur.execute('INSERT INTO movies (doc) VALUES (%s)', (json_str,))

  conn.commit()
  cur.close()
  conn.close()

main()
