SET job.name 'sophie_samplevel_to_hbase'
sample_all = LOAD 'gfs_vel_in/v20140426.csv' USING PigStorage(',') AS (day:chararray, hour:int, latlong:chararray, velocity:double);
sample_grp = GROUP sample_all BY (day, latlong);
sample_avg = FOREACH sample_grp GENERATE group.latlong, AVG(sample_all.velocity) as avgvel;
STORE sample_avg INTO 'hbase://samplevel1' USING org.apache.pig.backend.hadoop.hbase.HBaseStorage('data:d20140426');