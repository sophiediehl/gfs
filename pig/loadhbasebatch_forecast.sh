#!/bin/bash

year=2014
month=9
day=22
date=$(python getday.py $year $month $day)
python makeforcput.py $date
pig forecast_to_hbase.pig

