#!/bin/bash

year=2013

# Monthly averages to hbase
for month in {9..12}
do
  python ../pig/makemonthput.py $year $month
  pig monthavg_to_hbase.pig
done

