
-- SET job.name 'test_job';

vel_day = LOAD 'gfs_vel_new/x20140101.csv' USING PigStorage(',') AS (day:chararray, hour:int, la:double, lo:double, velocity:double);

fil_vel_day = FILTER vel_day BY (((la <= 49 AND la >= 38) AND (lo >= 235.5 AND lo <= 293))
  OR ((la >= 25.0 AND la <= 38) AND (lo >= 236.5 and lo <= 285.5)));
--  AND (la / 0.5 == 0 AND lo / 0.5 == 0);

vel_grp = GROUP fil_vel_day BY (day, la, lo);
-- vel_grp: {group: (day: chararray,la: double,lo: double),
--  fil_vel_day: {(day: chararray,hour: int,la: double,
--    lo: double,velocity: double)}}

avg_day = FOREACH vel_grp GENERATE group.la*10000+group.lo as latlong, 
  ROUND((AVG(fil_vel_day.velocity))*1000.0)/1000.0 as avgvel;

STORE avg_day INTO 'hbase://testtable' USING org.apache.pig.backend.hadoop.hbase.HBaseStorage('d:f1');

