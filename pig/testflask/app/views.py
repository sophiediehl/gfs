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

@app.route('/testytest')
def testytest():
  # Data from the hbase table, just for Jan 1, 2014
  rows = {}
  #row = wvel.row('37.5_237.5', columns=['data:d20140101'])
  #vel_in2.append(row['data:d20140101'])
  # Sample map data (lat, long, velocity [m/s])  
  vel_in = [] \
    #(37.5, 237.5, 10.0),\
    #(37.5, 237.0, 2.0),\
    #(38.0, 237.5, 2.0),\
    #(38.0, 237.0, 2.0)\
  lalo = [("37.5","237.5"),("37.5","237.0"),\
	("38.0", "237.5"),("38.0", "237.0")]
  for (la, lo) in lalo:
    row = wvel.row(la+'_'+lo)
    rows[(la, lo)] = row
    vel_in.append((float(la), float(lo), float(row['data:d20140101'])))

  return render_template("testytest.html", 
	vel_in = vel_in)

