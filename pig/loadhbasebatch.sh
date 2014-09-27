#!/bin/bash

year=2014

for month in 1 3 5 7 8
do
  for day in {1..31}
  do
    day=$(python getday.py $year $month $day)
    python makepigput.py $day
    pig allwindskinny_to_hbase.pig
  done
done

for month in 4 6
do
  for day in {1..30}
  do
    day=$(python getday.py $year $month $day)
    python makepigput.py $day
    pig allwindskinny_to_hbase.pig
  done
done

for month in 2
do
  for day in {1..28}
  do
    day=$(python getday.py $year $month $day)
    python makepigput.py $day
    pig allwindskinny_to_hbase.pig
  done
done

for month in 9
do
  for day in {1..23}
  do
    day=$(python getday.py $year $month $day)
    python makepigput.py $day
    pig allwindskinny_to_hbase.pig
  done
done

