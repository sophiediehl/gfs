#!/bin/bash

# get several months worth of data
year=2013

for month in 9 11
do
    for day in {1..30}
    do
        for ihour in {0..7}
        do
            url=$(python getwgeturl.py $year $month $day $ihour)
            wget $url --limit-rate=800k -P gfs_rawdata
        done
        # process the data
        filen=$(python processraw.py $year $month $day)

        # store processed data in hdfs
        hdfs dfs -put $filen gfs_vel_in

        # delete processed and unprocessed from aws
        rm gfs_hdfs_in/*
        hdfs dfs -put gfs_rawdata/* gfs_rawdata
        rm gfs_rawdata/*
    done
done

for month in 10 12
do
    for day in {1..31}
    do
        for ihour in {0..7}
        do
            url=$(python getwgeturl.py $year $month $day $ihour)
            wget $url --limit-rate=800k -P gfs_rawdata
        done
        # process the data
        filen=$(python processraw.py $year $month $day)

        # store processed data in hdfs
        hdfs dfs -put $filen gfs_vel_in

        # delete processed and unprocessed from aws
        rm gfs_hdfs_in/*
        hdfs dfs -put gfs_rawdata/* gfs_rawdata
        rm gfs_rawdata/*
    done
done


