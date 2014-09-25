from numpy import arange, tile, repeat
from flask import render_template, request, redirect
from app import app
import happybase
connection = happybase.Connection()
wvel = connection.table('allwindskinny')

region_data = { \
  'CONUS': {'latmin': 25.5, 'latmax': 49.5, \
    'longmin': 235, 'longmax': 293.5, \
    'step': 0.5, 'center': (38.0, 263.0)}, \
  'WORLD': {'latmin': -80.0, 'latmax': 80.0,
    'longmin': 10.0, 'longmax': 350.0, \
    'step': 4.0, 'center': (0.0, 180.0)} \
}

@app.route('/')
@app.route('/index')
def index():
  return render_template("viewform.html")

@app.route('/processform', methods=['POST'])
def processform():
  region = request.form.getlist('region')[0]
  day = request.form.getlist('day')[0]
  return redirect('/reg/'+region+'/day/'+day)

@app.route('/reg/<region>/day/<day>')
def showheatmap(region, day):
  latmin = region_data[region]['latmin']
  latmax =  region_data[region]['latmax']
  longmin = region_data[region]['longmin']
  longmax =  region_data[region]['longmax']
  step = region_data[region]['step']
  center = region_data[region]['center']
  vel_in = loadarea(latmin, latmax, longmin, \
	longmax, step, day)
  return render_template("loadarea.html",
	vel_in = vel_in,
	center = center,
	title = "Wind Speed in m/s") 

@app.route('/conus')
def conus():
  # Lat/long range of geographic area to plot
  day = '20140101'
  latmin = 25.5 # CONUS: 25.5
  latmax = 49.5 # CONUS: 49.5
  longmin = 235 # CONUS: 235
  longmax = 293.5 # CONUS: 293.5
  step = 0.5 # Geographic granularity
  center = (38.0, 263.0)
  vel_in = loadarea(latmin, latmax, longmin, \
	longmax, step, day)
  return render_template("loadarea.html", 
	vel_in = vel_in, 
	center = center,
	title = "Continental United States")

def loadarea(latmin, latmax, longmin, longmax, step, day):
  vel_in = [] 
  las = arange(latmin, latmax, step)
  los = arange(longmin, longmax, step)
  lalo = zip(repeat(las, len(los)),tile(los, len(las)))
  for (la, lo) in lalo:
    row = wvel.row(str(la)+'_'+str(lo)+'_'+day)
    vel_in.append((la, lo, float(row['d:v80m'])))
  return vel_in
