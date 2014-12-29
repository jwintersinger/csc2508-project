#!/bin/bash
time (cat /mnt/brussels/tmp/movies_1m.json | ./postgres_inserter.py)
