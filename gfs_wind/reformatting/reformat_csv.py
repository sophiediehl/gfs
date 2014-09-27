import sys

# Reformat files stored in hdfs so lat and long
# can be accessed as separate floats
def reformatter(year, month, day): # i.e. '2014', '9', '5'
  if len(month) < 2: month = "0" + month
  if len(day) < 2: day = "0" + day
  timestr = year + month + day
  old_file = open('format_old/v'+timestr+'.csv','r')
  new_file = open('format_new/x'+timestr+'.csv','w')
  # Split latlong string into lat, long floats
  contents = old_file.read()
  new_file.write(contents.replace('_',','))
  # Close both files
  old_file.close()
  new_file.close()

if __name__ == "__main__":
  reformatter(sys.argv[1],sys.argv[2],sys.argv[3])

