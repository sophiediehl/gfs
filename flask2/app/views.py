from numpy import arange, tile, repeat
from flask import render_template, request, redirect
from app import app
import happybase
connection = happybase.Connection()
wvel = connection.table('allwindskinny')

@app.route('/')
@app.route('/index')
def index():
  regions = [(region, region_data[region]['name']) \
	for region in region_data]
  return render_template("pickarea.html",
	regions = regions)

@app.route('/view/<la>/<lo>/<ttype>/<tunit>')
def viewarea(la, lo, ttype, tunit):
  center = (float(la), float(lo))
  vel_in = loadarea(float(la), float(lo), ttype, tunit)
  return render_template("bsexample.html",
	vel_in = vel_in,
	center = center,
	title = "Wind Speed in Meters per Second")

def loadarea(la, lo, ttype, tunit):
  lastep = 0.5
  lostep = 0.5
  vel_in = [] 
  las = arange(la-6, la+6, lastep)
  los = arange(lo-12, lo+12, lostep)
  lalo = zip(repeat(las, len(los)),tile(los, len(las)))
  for (la, lo) in lalo:
    if ttype == 'D': # Daily average view
      row = wvel.row(tunit+'_'+str(la)+'_'+str(lo))
      vel_in.append((la, lo, float(row['d:v80m'])))
  return vel_in

