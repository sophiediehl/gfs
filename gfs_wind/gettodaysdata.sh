#!/bin/bash

# get today's data
year=`date +%Y`
month=`date +%m`
#day=`date +%d`
day=28 # WHERE IS GFS_MASTER?? DO I HAVE TO DO DAY-X W/REGULAR GFS4? EDIT GETWGETURL2.PY IF YOU FIND GFS_MASTER.

# Download from NOAA website
for ihour in {0..7}
do
  url=$(python getwgeturl2.py $year $month $day $ihour)
  wget $url -P gfs_rawdata2
done

# process the data
filen=$(python processraw2.py $year $month $day)
# store processed data in hdfs
hdfs dfs -put $filen gfs_vel_in
# delete processed and unprocessed from aws
rm gfs_hdfs_in2/*
hdfs dfs -put gfs_rawdata2/* gfs_rawdata
rm gfs_rawdata2/*

# put the daily average in allwindskinny
date=$(python ../pig/getday.py $year $month $day)
python ../pig/makepigput.py $date
pig allwindskinny_to_hbase.pig

# update the forecast file
python ../pig/makeforcput.py $date
pig forecast_to_hbase.pig

# If it's the first of the month,
# fill in monthly average table for previous month
if [[ $day == 1 ]];
then
  month=$(($month-1))
  if [[ $month -lt 0 ]]
  then
    month=12
    year=$(($year-1))
  fi
  python ../pig/makemonthput.pig $year $month
  pig monthavg_to_hbase.pig
fi

