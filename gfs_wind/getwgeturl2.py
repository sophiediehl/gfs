import sys

# Whole URL for NOAA gfs4 data.
def geturl(year, month, day, ihour): # all ints
  ihour = int(ihour)
  if len(month) < 2: month = "0" + month
  if len(day) < 2: day = "0" + day
  if ihour < 4: hour = "0" + str(3*ihour)
  else: hour = str(3*ihour)
  url = "www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs." + year + month + \
        day + "00/gfs.t00z.pgrb2f"+ hour
  return url

if __name__ == "__main__":
  print geturl(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])


# www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.2014093000/gfs.t00z.pgrb2f00
