import sys
import pygrib
import csv
import wget

def processor(year, month, day): # i.e. '2014', '9', '5'
  timeint = int(year)*10000 + int(month)*100 + int(day)
  if len(month) < 2: month = "0" + month
  if len(day) < 2: day = "0" + day
  timestr = year + month + day
  results = []

# # www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.2014093000/gfs.t00z.pgrb2f00

  for k in range(8):
    if k<4: fn = '/home/ubuntu/gfs/gfs_wind/gfs_rawdata2/gfs.t00z.pgrb2f0'+str(k*3)
    else: fn = '/home/ubuntu/gfs/gfs_wind/gfs_rawdata2/gfs.t00z.pgrb2f'+str(k*3)
    gr = pygrib.open(fn)
    # Select variables relevant to wind speed
    msu = gr.select(name='U component of wind', \
        typeOfLevel='heightAboveGround',level=80)
    msv = gr.select(name='V component of wind', \
        typeOfLevel='heightAboveGround',level=80)
    # Get values of UGRD and VGRD
    vu = msu[0].values
    vv = msv[0].values
    # Latitude and longitude matrices for 0.5 degree resolution
    lats, lons = msu[0].latlons()
    for i in range(361):
      for j in range(720):
        latlong = str(lats[i][j])+'_'+str(lons[i][j])
        velocity = round((vu[i][j]**2 + vv[i][j]**2)**0.5,5)
        results.append([timeint,k,latlong, velocity])
  # Write to output file
  with open('/home/ubuntu/gfs/gfs_wind/gfs_hdfs_in2/v'+timestr+'.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(results)
  return '/home/ubuntu/gfs/gfs_wind/gfs_hdfs_in2/v'+timestr+'.csv'

if __name__ == "__main__":
  print processor(sys.argv[1],sys.argv[2],sys.argv[3])

