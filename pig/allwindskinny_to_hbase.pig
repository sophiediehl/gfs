SET job.name 'sophie_allwind_to_hbase'
sample_all = LOAD 'gfs_vel_in/v2014.csv' USING PigStorage(',') AS (day:chararray, hour:int, latlong:chararray, velocity:double);
sample_grp = GROUP sample_all BY (day, latlong);
sample_avg = FOREACH sample_grp GENERATE CONCAT(CONCAT(group.day, '_'), group.latlong), ROUND((AVG(sample_all.velocity))*100.0)/100.0 as avgvel;
STORE sample_avg INTO 'hbase://allwindskinny' USING org.apache.pig.backend.hadoop.hbase.HBaseStorage('d:v80m');