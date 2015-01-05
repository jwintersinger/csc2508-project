#!/usr/bin/env python3
import re
import sys

def parse_time(timestr):
  timestr = timestr.strip()
  minutes, seconds = re.findall(r'^real (\d+)m([\d\.]+)s', timestr.strip())[0]
  parsed = 60 * int(minutes) + float(seconds)
  return parsed

def main():
  out_files = {
    'Postgres relational insert time': 'results.postgres_relational_queries.csv',
    'Postgres JSON insert time': 'results.postgres_json_queries.csv',
    'Mongo insert time': 'results.mongo_queries.csv',
  }
  for k in out_files.keys():
    out_files[k] = open(out_files[k], 'a')

  for line in sys.stdin:
    sys_name, timestr = line.strip().split(': ')
    seconds = parse_time(timestr)
    print('insert,%s' % seconds, file = out_files[sys_name])

  for k, v in out_files.items():
    v.close()

main()
