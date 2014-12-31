#!/bin/bash
set -euo pipefail

function load_mongo {
  input_file=$1
  mongo_insert_time=$(time (cat $input_file | mongoimport --drop --port 27017 --db pants --collection movies) 2>&1 1>/dev/null)
  echo "Mongo insert time: $mongo_insert_time" && echo
}

function load_postgres_json {
  input_file=$1
  postgres_insert_time=$(time (cat $input_file | ./postgres_json_inserter.py) 2>&1 1>/dev/null)
  echo "Postgres JSON insert time: $postgres_insert_time" && echo
}

function load_postgres_relational {
  input_file=$1
  postgres_insert_time=$(time (cat $input_file | ./postgres_relational_inserter.py) 2>&1 1>/dev/null)
  echo "Postgres relational insert time: $postgres_insert_time" && echo
}

function run_mongo {
  ./mongo_queries.py 1>/dev/null 2>results.mongo_queries.csv
}

function run_postgres_json {
  ./postgres_json_queries.py 1>/dev/null 2>results.postgres_json_queries.csv
}

function run_postgres_relational {
  ./postgres_relational_queries.py 1>/dev/null 2>results.postgres_relational_queries.csv
}

function main {
  load_mongo $1
  load_postgres_json $1
  load_postgres_relational $1
  wait

  run_mongo
  run_postgres_json
  run_postgres_relational
  wait
}

main data/movies_100k.json
