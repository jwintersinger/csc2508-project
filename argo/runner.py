#!/usr/bin/env python22
import json
import sys

import psycopg2
import dbms_postgres
import argodb
import timeit
import random


def get_db():
  conn = psycopg2.connect("user=postgres dbname=argo")
  dbms = dbms_postgres.PostgresDBMS(conn)
  use_argo_1 = False
  return (conn, argodb.ArgoDB(dbms, use_argo_1))

def import_json(jsonfd):
  conn, db = get_db()
  records = json.load(jsonfd)

  for rec in records:
    query = 'INSERT INTO weiner OBJECT %s' % json.dumps(rec)
    result = db.execute_sql(query)
    for res in result:
      pass
      #print(json.dumps(result))

  conn.commit()

def run_shell():
  import readline

  conn, db = get_db()
  while True:
    try:
      sql_text = raw_input("Argo> ")
    except EOFError:
      print ""
      break
    try:
      for item in db.execute_sql(sql_text):
        print(json.dumps(item))
        print("DONE")
    except Exception, e:
      print("ERROR: %s" %e)

class Benchmark:
  def __init__(self, rec_strs_fn):
    conn, db = get_db()
    self._db = db
    self._tbl = 'test'

    with open(rec_strs_fn) as rec_strs_fd:
      self._rec_strs = json.load(rec_strs_fd)

    self._total_objs = 1000

  def _execute_query(self, query):
    result = self._db.execute_sql(query)
    for res in result:
      pass

  def _get_rec_str(self):
    return random.choice(self._rec_strs)

  def _get_num(self):
    num_objs = self._total_objs / 1000
    floor = random.randint(0, self._total_objs - num_objs)
    ceiling = floor + num_objs - 1
    return (floor, ceiling)

  def q1(self):
    self._execute_query('SELECT str1, num FROM %s' % self._tbl)

  def q2(self):
    self._execute_query('SELECT nested_obj.str1, nested_obj.num FROM %s' % self._tbl)

  def q3(self):
    self._execute_query('SELECT nested_obj.str1, nested_obj.num FROM %s' % self._tbl)

  def q4(self):
    xx = random.randint(0, 99)
    yy = random.randint(0, 99)
    self._execute_query('SELECT sparse_%s0, sparse_%s0 FROM %s' % (xx, yy, self._tbl))

  def q5(self):
    self._execute_query('SELECT * FROM %s WHERE str1 = "%s"' % (self._tbl, self._get_rec_str()))

  def q6(self):
    floor, ceiling = self._get_num()
    self._execute_query('SELECT * FROM %s WHERE num BETWEEN %s AND %s' % (self._tbl, floor, ceiling))

  def q7(self):
    floor, ceiling = self._get_num()
    self._execute_query('SELECT * FROM %s WHERE dyn1 BETWEEN XXXXX AND YYYYY' % (self._tbl, floor, ceiling))

  def q8(self):
    self._execute_query('SELECT * FROM %s WHERE "%s" = ANY nested_arr' % (self._tbl, self._get_rec_str())

  def q9(self):
    self._execute_query('SELECT * FROM %s WHERE sparse_XXX = YYYYY' % self._tbl)

  def q10(self):
    self._execute_query('SELECT COUNT(*) FROM %s WHERE num BETWEEN XXXXX AND YYYYY GROUP BY thousandth' % self._tbl)

  def q11(self):
    self._execute_query('SELECT COUNT(*) FROM %s WHERE num BETWEEN XXXXX AND YYYYY GROUP BY thousandth' % self._tbl)


  def run(self):
    t = timeit.Timer(lambda: self.q1())
    print(t.repeat(repeat=3, number=5))
  

def main():
  #import_json(sys.stdin)
  run_shell()
  return
  bm = Benchmark('rec_strs.json')
  bm.run()

main()
