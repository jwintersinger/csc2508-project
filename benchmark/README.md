Running benchmark
=================

Prerequisites:
    
    * PostgreSQL >= 9.4.0
    * MongoDB
    * Python 3
    * PyMongo
    * psycopg2

First, open `run.sh` and uncomment call to `benchmark_insert`. Then:

    mkdir data
    ./generator.py 100000 > data/movies_100k.json
    ./run.sh > /tmp/insert-results
    cat /tmp/insert-results | ./proc_insert_times.py

Now, open `run.sh` and comment out call to `benchmark_insert`, then uncomment
call to `benchmark_select`. Then:

    ./run.sh # Results written to results.*.csv files in current directory.
    ./plot_results.py # PNG files created in current directory.
