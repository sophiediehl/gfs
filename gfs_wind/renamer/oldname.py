import sys

def oldfilename(year, month, day): # i.e. '2014', '9', '5'
  if len(month) < 2: month = "0" + month
  if len(day) < 2: day = "0" + day
  timestr = year + month + day
  return 'gfs_vel_in/v'+timestr+'.csv'

if __name__ == "__main__":
  print oldfilename(sys.argv[1],sys.argv[2],sys.argv[3])
