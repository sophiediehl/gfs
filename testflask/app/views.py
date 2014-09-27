from numpy import arange, tile, repeat
from flask import render_template, request, redirect
from app import app
import happybase
connection = happybase.Connection()
wvel = connection.table('allwindskinny')

region_data = { \
  'GB': {'name': 'Great Britain', \
    'latmin': 50.0, 'latmax': 58.0, \
    'longmin': 349.5, 'longmax': 360.0, \
    'lostep': 1.0, 'center': (53.5, 356)}, \
  'CONUS': {'name': "Continental U.S.", \
    'latmin': 25.5, 'latmax': 49.5, \
    'longmin': 235, 'longmax': 293.5, \
    'lostep': 0.5, 'center': (38.0, 263.0)}, \
  'EUSO': {'name': 'Europe - South', \
    'latmin': 25.5, 'latmax': 49.5, \
    'longmin': 235, 'longmax': 293.5, \
    'lostep': 0.5, 'center': (38.0, 263.0)}, \
  'EUNO': {'name': 'Europe - Nordic', \
    'latmin': 25.5, 'latmax': 49.5, \
    'longmin': 235, 'longmax': 293.5, \
    'lostep': 0.5, 'center': (38.0, 263.0)}, \
  'AFNO': {'name': 'Africa - North', \
    'latmin': 25.5, 'latmax': 49.5, \
    'longmin': 235, 'longmax': 293.5, \
    'lostep': 0.5, 'center': (38.0, 263.0)}, \
  'AFSO': {'name': 'Africa - South', \
    'latmin': 25.5, 'latmax': 49.5, \
    'longmin': 235, 'longmax': 293.5, \
    'lostep': 0.5, 'center': (38.0, 263.0)}, \
  'ALA': {'name': 'Alaska and Yukon', \
    'latmin': 25.5, 'latmax': 49.5, \
    'longmin': 235, 'longmax': 293.5, \
    'lostep': 0.5, 'center': (38.0, 263.0)}, \
  'CAN': {'name': 'Canada', \
    'latmin': 25.5, 'latmax': 49.5, \
    'longmin': 235, 'longmax': 293.5, \
    'lostep': 0.5, 'center': (38.0, 263.0)}, \
  'CAM': {'name': 'Central America', \
    'latmin': 1.0, 'latmax': 24.5, \
    'longmin': 252.0, 'longmax': 311.0, \
    'lostep': 0.5, 'center': (38.0, 263.0)}, \
  'SSA': {'name': 'South America', \
    'latmin': -36.0, 'latmax': -0.5, \
    'longmin': 277.0, 'longmax': 325.5, \
    'lostep': 0.5, 'center': (38.0, 263.0)}, \
  'AUS': {'name': 'Australia', \
    'latmin': -44.0, 'latmax': -9.0, \
    'longmin': 112.0, 'longmax': 156.5, \
    'lostep': 0.5, 'center': (-26.0, 134.5)}, \
  'ME': {'name': 'Middle East', \
    'latmin': 14.0, 'latmax': 41.0, \
    'longmin': 24.5, 'longmax': 77.5, \
    'lostep': 0.5, 'center': (29.0, 52.0)}, \
  'SEA': {'name': 'Asia - Southeast', \
    'latmin': 6.0, 'latmax': 34.5, \
    'longmin': 70.0, 'longmax': 126.0, \
    'lostep': 0.5, 'center': (23.5, 98.0)}, \
  'NEA': {'name': 'Asia: Northeast', \
    'latmin': 29.5, 'latmax': 52.5, \
    'longmin': 89, 'longmax': 147.5, \
    'lostep': 0.5, 'center': (41.5, 114.5)}, \
}

@app.route('/')
@app.route('/index')
def index():
  regions = [(region, region_data[region]['name']) \
	for region in region_data]
  return render_template("viewform.html",
	regions = regions)

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
  lastep = 0.5
  lostep = region_data[region]['lostep']
  center = region_data[region]['center']
  vel_in = loadarea(latmin, latmax, longmin, \
	longmax, lostep, day)
  regions = [(reg, region_data[reg]['name']) \
        for reg in region_data]
  return render_template("loadarea.html",
	vel_in = vel_in,
	center = center,
	title = "Wind Speed in Meters per Second",
	regions = regions) 

def loadarea(latmin, latmax, longmin, longmax, lostep, day):
  vel_in = [] 
  las = arange(latmin, latmax, 0.5)
  los = arange(longmin, longmax, lostep)
  lalo = zip(repeat(las, len(los)),tile(los, len(las)))
  for (la, lo) in lalo:
    row = wvel.row(day+'_'+str(la)+'_'+str(lo))
    vel_in.append((la, lo, float(row['d:v80m'])))
  return vel_in
