from numpy import arange, tile, repeat
from flask import render_template
from app import app
import happybase
connection = happybase.Connection()
wvel = connection.table('samplevel1')

@app.route('/')
@app.route('/index')
def index():
  return "Getcher wind data right here."

@app.route('/latlong/<path>')
def latlong(path):
  key = path
  row = wvel.row(key)
  return row['data:d20140101'] + '  and  ' + row['data:d20140102']

@app.route('/conus')
def conus():
  # Lat/long range of geographic area to plot
  latmin = 25.5 # CONUS: 25.5
  latmax = 49.5 # CONUS: 49.5
  longmin = 235 # CONUS: 235
  longmax = 293.5 # CONUS: 293.5
  step = 0.5 # Geographic granularity
  center = (38.0, 263.0)
  (vel_in, rows) = loadarea(latmin, latmax, longmin, \
	longmax, step)
  return render_template("loadarea.html", 
	vel_in = vel_in, 
	center = center,
	title = "Continental United States")

def loadarea(latmin, latmax, longmin, longmax, step):
  # Data from the hbase table, just for Jan 1, 2014
  rows = {}
  vel_in = [] 
  las = arange(latmin, latmax, step)
  los = arange(longmin, longmax, step)
  lalo = zip(repeat(las, len(los)),tile(los, len(las)))
  for (la, lo) in lalo:
    row = wvel.row(str(la)+'_'+str(lo))
    rows[(la, lo)] = row
    vel_in.append((la, lo, float(row['data:d20140101'])))
  return (vel_in, rows)
