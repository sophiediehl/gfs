#!/bin/bash

# get today's data
year=`/bin/date +%Y`
month=`/bin/date +%m`
day=`/bin/date +%d`

# Download from NOAA website
for ihour in {0..7}
do
  url=$(/usr/bin/python /home/ubuntu/gfs/gfs_wind/getwgeturl2.py $year $month $day $ihour)
  /usr/bin/wget $url --limit-rate=800k -P /home/ubuntu/gfs/gfs_wind/gfs_rawdata2
done

# process the data
filen=$(/usr/bin/python /home/ubuntu/gfs/gfs_wind/processraw2.py $year $month $day)
# store processed data in hdfs
/usr/bin/hdfs dfs -put $filen gfs_vel_in
# delete processed and unprocessed from aws
/bin/rm /home/ubuntu/gfs/gfs_wind/gfs_hdfs_in2/*
/usr/bin/hdfs dfs -put /home/ubuntu/gfs/gfs_wind/gfs_rawdata2/* gfs_rawdata
/bin/rm /home/ubuntu/gfs/gfs_wind/gfs_rawdata2/*

# put the daily average in allwindskinny
date=$(/usr/bin/python /home/ubuntu/gfs/gfs_wind/../pig/getday.py $year $month $day)
/usr/bin/python /home/ubuntu/gfs/gfs_wind/../pig/makepigput.py $date
/usr/bin/pig /home/ubuntu/gfs/gfs_wind/allwindskinny_to_hbase.pig

# update the forecast file
/usr/bin/python /home/ubuntu/gfs/gfs_wind/../pig/makeforcput.py $date
/usr/bin/pig /home/ubuntu/gfs/gfs_wind/forecast_to_hbase.pig

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
  /usr/bin/python /home/ubuntu/gfs/gfs_wind/../pig/makemonthput.py $year $month
  /usr/bin/pig /home/ubuntu/gfs/gfs_wind/monthavg_to_hbase.pig
fi

