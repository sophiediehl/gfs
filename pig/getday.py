import sys

def getday(year, month, day):
  if len(month) < 2: month = "0"+month
  if len(day) < 2: day = "0"+day
  return year+month+day

if __name__ == "__main__":
  print getday(sys.argv[1], sys.argv[2], sys.argv[3])
