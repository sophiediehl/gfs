#!/bin/bash

# Reformat several months of data
# to split latlong string into lat, long floats

year=2014

for month in 1
do
  for day in {1..8}
  do
    hdfs dfs -get $(python renamer/oldname.py $year $month $day) format_old/
    python reformat_csv.py $year $month $day
    hdfs dfs -put $(python renamer/newname.py $year $month $day) gfs_vel_new/
  done
done
