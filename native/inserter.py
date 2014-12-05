import json
import psycopg2
import sys

def main():
  conn = psycopg2.connect("dbname=postgres user=postgres")
  cur = conn.cursor()
  cur.execute('DELETE FROM moviesj');

  recs = json.load(sys.stdin)
  for rec in recs:
    json_str = json.dumps(rec)
    cur.execute('INSERT INTO moviesj (data) VALUES (%s)', (json_str,))

  conn.commit()
  cur.close()
  conn.close()

main()
