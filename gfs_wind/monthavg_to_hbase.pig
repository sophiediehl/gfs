SET job.name 'sophie_monthavg_to_hbase'
sample_all = LOAD 'gfs_vel_in/v201312*' USING PigStorage(',') AS (day:chararray, hour:int, latlong:chararray, velocity:double);
sample_grp = GROUP sample_all BY latlong;
sample_avg = FOREACH sample_grp GENERATE group, ROUND((AVG(sample_all.velocity))*100.0)/100.0 as avgvel;
STORE sample_avg INTO 'hbase://v201312' USING org.apache.pig.backend.hadoop.hbase.HBaseStorage('d:v80m');