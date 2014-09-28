from numpy import arange, tile, repeat
from flask import render_template, request, redirect
from app import app
import happybase
connection = happybase.Connection()
wvel = connection.table('allwindskinny')

# Number of days in each month
modaynominal = {'Jan':('01',31), 'Feb':('02',28), \
	'Mar':('03',31), 'Apr':('04',30), 'May':('05',31), \
	'Jun':('06',30), 'Jul':('07',31), 'Aug':('08',31), \
	'Sep':('09',30), 'Oct':('10',31), 'Nov':('11',30), \
	'Dec':('12',31)}
mos = ['Jan','Feb','Mar','Apr','May','Jun','Jul', \
	'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


@app.route('/')
@app.route('/index')
def index():
  return render_template("pickarea.html")

@app.route('/view/<la>/<lo>/<ttype>/<tunit>')
def viewarea(la, lo, ttype, tunit):
  center = (float(la), float(lo))
  vel_in = loadarea(float(la), float(lo), ttype, tunit)
  return render_template("bsexample.html",
	year = 2014, # current year -1 
	ttype = ttype,
	tunit = tunit,
	vel_in = vel_in,
	center = center,
	months = mos,
	moinfo = modaynominal,
	title = "Wind Speed in Meters per Second")

def loadarea(la, lo, ttype, tunit):
  lastep = 0.5
  lostep = 0.5
  vel_in = [] 
  las = arange(la-6, la+6, lastep)
  los = arange(lo-12, lo+12, lostep)
  lalo = zip(repeat(las, len(los)),tile(los, len(las)))
  for (la, lo) in lalo:
    la = ((la + 90) % 180) - 90 # No falling off the edge
    lo = lo % 360		# of the world!
    if ttype == 'D': # Daily average view
      row = wvel.row(tunit+'_'+str(la)+'_'+str(lo))
      vel_in.append((la, lo, float(row['d:v80m'])))
  return vel_in

