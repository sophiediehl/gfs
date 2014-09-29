#!/bin/bash

year=2014

for month in 9
do
 for day in {1..23}
  do
    date=$(python getday.py $year $month $day)
    python makepigput.py $date
    pig allwindskinny_to_hbase.pig
  done
done

