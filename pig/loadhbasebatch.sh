#!/bin/bash

year=2014

for month in 2 3 4 5 6 7 8
do
  python makemonthput.py $year $month
  pig monthavg_to_hbase.pig
done
