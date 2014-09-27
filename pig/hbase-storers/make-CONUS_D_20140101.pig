SET jobi.name 'CONUS_D_20140101';

vel_day = LOAD 'gfs_vel_new/x20140101.csv' USING PigStorage(',') AS (day:chararray, hour:int, lat: float, long:float, velocity:double);

sample_grp = GROUP sample_all BY (day, lat, long) WHERE;

sample_avg = FOREACH sample_grp GENERATE group.latlong, AVG(sample_all.velocity) as avgvel;

STORE sample_avg INTO 'hbase://allwind' USING org.apache.pig.backend.hadoop.hbase.HBaseStorage('data:d20140228');
