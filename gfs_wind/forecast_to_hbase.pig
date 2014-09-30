SET job.name 'sophie_forecast_to_hbase'
sample_all = LOAD 'gfs_vel_in/v20140929.csv' USING PigStorage(',') AS (day:chararray, hour:chararray, latlong:chararray, velocity:double);
sample_grp = GROUP sample_all BY (hour, latlong);
sample_avg = FOREACH sample_grp GENERATE CONCAT(CONCAT(group.hour, '_'), group.latlong), ROUND((AVG(sample_all.velocity))*100.0)/100.0 as avgvel;
STORE sample_avg INTO 'hbase://forecast' USING org.apache.pig.backend.hadoop.hbase.HBaseStorage('d:v80m');