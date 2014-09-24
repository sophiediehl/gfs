import sys

datestr = sys.argv[1]

contents = "SET job.name 'sophie_samplevel_to_hbase'\nsample_all = LOAD 'gfs_vel_in/v"+datestr+".csv' USING PigStorage(',') AS (day:chararray, hour:int, latlong:chararray, velocity:double);\nsample_grp = GROUP sample_all BY (day, latlong);\nsample_avg = FOREACH sample_grp GENERATE group.latlong, AVG(sample_all.velocity) as avgvel;\nSTORE sample_avg INTO 'hbase://samplevel1' USING org.apache.pig.backend.hadoop.hbase.HBaseStorage('data:d"+datestr+"');"

f = open('samplevel_to_hbase.pig', 'w')
f.write(contents)
f.close()


