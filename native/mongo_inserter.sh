#!/bin/bash
time (cat /mnt/brussels/tmp/movies_1m.json | mongoimport --drop --db pants --collection movies)
