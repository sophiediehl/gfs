-- sample_to_hbase.pig
-- Can I dynamically name hbase columns when writing from pig?

SET job.name 'sophie2_sample_to_hbase'

sample_data = LOAD 'sample_gfs/sample.txt' USING PigStorage(',') AS (first:chararray,second:int);

STORE sample_data INTO 'hbase://testtable'
USING org.apache.pig.backend.hadoop.hbase.HBaseStorage(
'data:third'
);

