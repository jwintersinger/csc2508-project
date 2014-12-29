function main {
  input_file=$1

  mongo_insert_time=$(time (cat $input_file | mongoimport --drop --db pants --collection movies) 2>&1 1>/dev/null)
  postgres_insert_time=$(time (cat $input_file | ./postgres_inserter.py) 2>&1 1>/dev/null)
  
  mongo_query_time=$(time (./mongo_queries.py) 2>&1 1>/dev/null)
  postgres_query_time=$(time (./postgres_queries.py) 2>&1 1>/dev/null)
  
  echo "Mongo insert time: $mongo_insert_time"
  echo "Postgres insert time: $postgres_insert_time"
  echo "Mongo query time: $mongo_query_time"
  echo "Postgres query time: $postgres_query_time"
}

main $1
