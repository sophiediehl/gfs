import sys

datestr = sys.argv[1]

contents = "SET job.name 'sophie_allwind_to_hbase'\nsample_all = LOAD 'gfs_vel_in/v"+datestr+".csv' USING PigStorage(',') AS (day:chararray, hour:int, latlong:chararray, velocity:double);\nsample_grp = GROUP sample_all BY (day, latlong);\nsample_avg = FOREACH sample_grp GENERATE CONCAT(CONCAT(group.day, '_'), group.latlong), ROUND((AVG(sample_all.velocity))*100.0)/100.0 as avgvel;\nSTORE sample_avg INTO 'hbase://allwindskinny' USING org.apache.pig.backend.hadoop.hbase.HBaseStorage('d:v80m');"

f = open('allwindskinny_to_hbase.pig', 'w')
f.write(contents)
f.close()


