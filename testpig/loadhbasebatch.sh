#!/bin/bash

year=2014

for month in 2
do
  for day in {17..28}
  do
    day=$(python getday.py $year $month $day)
    python makepigput.py $day
    pig samplevel_to_hbase.pig
  done
done

for month in 3
do
  for day in {1..23} {25..28}
  do
    day=$(python getday.py $year $month $day)
    python makepigput.py $day
    pig samplevel_to_hbase.pig
  done
done

for month in 4
do
  for day in {1..26}
  do
    day=$(python getday.py $year $month $day)
    python makepigput.py $day
    pig samplevel_to_hbase.pig
  done
done

