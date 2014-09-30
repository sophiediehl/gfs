from numpy import arange, tile, repeat
from flask import render_template, request, redirect
from app import app
import happybase
import datetime
import pytz
connection = happybase.Connection()
wvel = connection.table('allwindskinny')
forecast = connection.table('forecast')

def generate_monthtables(y1,m1,y2,m2):
  monthtables = {}
  for month in range(m1,13):
    monthstr = "0"+str(month) if month<10 else str(month)
    monthkey = str(y1)+monthstr
    tablekey = "v"+str(y1)+str(month)
    monthtables[monthkey] = connection.table(tablekey)
  for month in range(1,m2+1):
    monthstr = "0"+str(month) if month<10 else str(month)
    monthkey = str(y2)+monthstr
    tablekey = "v"+str(y2)+str(month)
    monthtables[monthkey] = connection.table(tablekey)
  return monthtables

monthtables = generate_monthtables(2013,9,2014,12)

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
  now = datetime.datetime.now(pytz.timezone('US/Pacific'))
  return render_template("pickarea.html",
	curyear = now.year,
	curmo = now.month,
	curday = now.day)

@app.route('/slides')
def slides():
  return render_template("slides.html")

@app.route('/about')
def about():
  return render_template("about.html")

@app.route('/view/<la>/<lo>/<ttype>/<tunit>')
def viewarea(la, lo, ttype, tunit):
  now = datetime.datetime.now(pytz.timezone('US/Pacific'))
  center = (float(la), float(lo))
  vel_in = loadarea(float(la), float(lo), ttype, tunit)
  return render_template("bsexample.html",
	curyear = now.year,
	curmo = now.month,
	curday = now.day,
	moinfo = modaynominal,
	months = mos,
	ttype = ttype,
	tunit = tunit,
	hour = int(tunit[-1])*3,
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
    la = ((la + 90) % 180) - 90 # No falling off the edge
    lo = lo % 360		# of the world!
    if ttype == 'M': # Monthly average view
      row = monthtables[tunit].row(str(la)+'_'+str(lo))
      vel_in.append((la, lo, float(row['d:v80m'])))
    elif ttype == 'D': # Daily average view
      row = wvel.row(tunit+'_'+str(la)+'_'+str(lo))
      vel_in.append((la, lo, float(row['d:v80m'])))
    elif ttype == 'F':
      row = forecast.row(tunit[8]+'_'+str(la)+'_'+str(lo))
      vel_in.append((la, lo, float(row['d:v80m'])))
  return vel_in

