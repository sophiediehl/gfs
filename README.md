Windpipe, by Sophie Diehl: a data pipeline for wind speeds at the altitude of wind turbines (80 meters in the air).

I built this project as part of the Insight Data Engineering fellowship program, as an opportunity to try out big data pipelining tools such as HDFS, Pig, and HBase, as well as to satisfy my curiosity about the variability of turbine-altitude winds over time and space.

It can be viewed at
http://54.193.64.222:5000/
until October 17th.

Data comes from the National Oceanic and Atmospheric Administration's GFS4 modeling system, which provides forecasts in 3-hour intervals at a spatial resolution of 0.5 degrees latitude and longitude, released in daily batches. Data is available at
http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/
