#!/bin/bash
set -uo pipefail

mongo_port=27017
toro_port=27018
mongo_db_name=movies
postgres_json_db_name=movies_json
postgres_relational_db_name=movies_relational

function load_mongo {
  input_file=$1
  portno=$2
  system_type=$3

  mongo --eval "db.movies.drop()" --port $portno $mongo_db_name > /dev/null 2>&1
  mongo_insert_time=$(time (cat $input_file | mongoimport --drop --port $portno --db $mongo_db_name --collection movies) 2>&1 1>/dev/null)
  echo "$system_type insert time: " $mongo_insert_time
}

function load_postgres_json {
  input_file=$1

  dropdb -U postgres $postgres_json_db_name > /dev/null 2>&1
  createdb -U postgres $postgres_json_db_name
  postgres_insert_time=$(time (cat $input_file | ./postgres_json_inserter.py $postgres_json_db_name) 2>&1 1>/dev/null)
  echo "Postgres JSON insert time: " $postgres_insert_time
}

function load_postgres_relational {
  input_file=$1

  dropdb -U postgres $postgres_relational_db_name > /dev/null 2>&1
  createdb -U postgres $postgres_relational_db_name
  postgres_insert_time=$(time (cat $input_file | ./postgres_relational_inserter.py $postgres_relational_db_name) 2>&1 1>/dev/null)
  echo "Postgres relational insert time: " $postgres_insert_time
}

function run_mongo {
  portno=$1
  out_filename=$2
  ./mongo_queries.py $mongo_db_name $portno 1>/dev/null 2>$out_filename
}

function run_postgres_json {
  ./postgres_json_queries.py $postgres_json_db_name 1>/dev/null 2>results.postgres_json_queries.csv
}

function run_postgres_relational {
  ./postgres_relational_queries.py $postgres_relational_db_name 1>/dev/null 2>results.postgres_relational_queries.csv
}

function insert_records {
  load_postgres_json $1 &
  load_postgres_relational $1 &
  load_mongo $1 $mongo_port Mongo &
  #load_mongo $1 $toro_port Toro
  wait
}

function benchmark_insert {
  for foo in $(seq 10); do
    insert_records $1
  done
}

function benchmark_select {
  insert_records $1
  #run_postgres_json
  #run_postgres_relational
  #run_mongo $mongo_port results.mongo_queries.csv
  #run_mongo $toro_port results.toro_queries.csv
  wait
}

function main {
  #benchmark_insert $1
  benchmark_select $1
}

main data/movies_100k.json
