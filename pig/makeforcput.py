import sys

datestr = sys.argv[1]

contents = "SET job.name 'sophie_forecast_to_hbase'\nsample_all = LOAD 'gfs_vel_in/v"+datestr+".csv' USING PigStorage(',') AS (day:chararray, hour:chararray, latlong:chararray, velocity:double);\nsample_grp = GROUP sample_all BY (hour, latlong);\nsample_avg = FOREACH sample_grp GENERATE CONCAT(CONCAT(group.hour, '_'), group.latlong), ROUND((AVG(sample_all.velocity))*100.0)/100.0 as avgvel;\nSTORE sample_avg INTO 'hbase://forecast' USING org.apache.pig.backend.hadoop.hbase.HBaseStorage('d:v80m');"

f = open('/home/ubuntu/gfs/gfs_wind/forecast_to_hbase.pig', 'w')
f.write(contents)
f.close()


