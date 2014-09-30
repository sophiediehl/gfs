import sys

year = sys.argv[1]
month = sys.argv[2]
monthst=month[:]
if len(monthst)<2: monthst='0'+month

contents = "SET job.name 'sophie_monthavg_to_hbase'\nsample_all = LOAD 'gfs_vel_in/v"+year+monthst+"*' USING PigStorage(',') AS (day:chararray, hour:int, latlong:chararray, velocity:double);\nsample_grp = GROUP sample_all BY latlong;\nsample_avg = FOREACH sample_grp GENERATE group, ROUND((AVG(sample_all.velocity))*100.0)/100.0 as avgvel;\nSTORE sample_avg INTO 'hbase://v"+year+month+"' USING org.apache.pig.backend.hadoop.hbase.HBaseStorage('d:v80m');"

f = open('/home/ubuntu/gfs/gfs_wind/monthavg_to_hbase.pig', 'w')
f.write(contents)
f.close()


