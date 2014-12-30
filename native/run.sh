#!/bin/bash
set -euo pipefail

function load_mongo {
  input_file=$1
  mongo_insert_time=$(time (cat $input_file | mongoimport --drop --port 27018 --db pants --collection movies) 2>&1 1>/dev/null)
  echo "Mongo insert time: $mongo_insert_time" && echo
}

function load_postgres {
  input_file=$1
  postgres_insert_time=$(time (cat $input_file | ./postgres_inserter.py) 2>&1 1>/dev/null)
  echo "Postgres insert time: $postgres_insert_time" && echo
}

function run_mongo {
  mongo_query_time=$(./mongo_queries.py 2>&1 1>/dev/null)
  echo -e "Mongo query time:\n$mongo_query_time\n"
}

function run_postgres {
  postgres_query_time=$(./postgres_queries.py 2>&1 1>/dev/null)
  echo -e "Postgres query time:\n$postgres_query_time\n"
}

function main {
  load_mongo $1
  #load_postgres $1
  #run_mongo &
  #run_postgres &
  wait
}

main data/movies_1k.json
