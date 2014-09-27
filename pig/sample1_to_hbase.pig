-- sample1_to_hbase.pig
-- Can I dynamically name hbase columns when writing from pig?
-- Can I even write a full day worth of average velocities to
-- hbase (full data size)?

SET job.name 'sophie2_sample1_to_hbase'

sample_data = LOAD 'sample_gfs/sample1.txt' USING PigStorage(',') AS (day:chararray,hour:int,latlong:chararray,velocity:double);


