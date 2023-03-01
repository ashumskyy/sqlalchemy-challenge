# Importing dependencies
import sqlite3 as sql
from flask import Flask, jsonify
import datetime as dt
import numpy as np

# Flask Setup
app = Flask(__name__)

# Calculate the date 1 year ago from last date in database
prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

####################
# Flask Routes
####################

# Welcome page
@app.route("/")
def welcome():
    return(
        f"<h2>Go to: <br><h2>"
        f"<ol><li><a href=http://127.0.0.1:5000/api/v1.0/precipitation>"
        f"Precipitation (/api/v1.0/precipitation)</a></li><br>"
        f"<li><a href=http://127.0.0.1:5000/api/v1.0/stations>"
        f"Stations (/api/v1.0/stations)</a></li><br>"
        f"<li><a href=http://127.0.0.1:5000/api/v1.0/tobs>"
        f"TOBS (/api/v1.0/tobs)</a></li><br>"
        f"<p>'start' and 'end' date should be in the format MMDDYYYY.</p><br>"
        f"<li>http://127.0.0.1:5000/api/v1.0/temp/<start></li></br>"
        f"<li>http://127.0.0.1:5000/api/v1.0/temp/<start>/<end>""</li></ol>"
    )

# Precipitation Page
@app.route("/api/v1.0/precipitation")

# Creating a Class
def precipitation():
    
    # Connectiong to sqlite with sqlite3
    with sql.connect("Resources/hawaii.sqlite") as con:
        
        # Connectiong to a cursor
        cur = con.cursor()
        
        # Performing a query
        cur.execute(f"SELECT date, prcp FROM measurement WHERE date > '{prev_year}' ORDER BY date")
        
        # Selecting our query
        rows = cur.fetchall()
    
    # Closing the connection    
    con.close()
    
    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(rows))
    
    # Jsonifying our result (temps)
    return jsonify(temps)

@app.route("/api/v1.0/stations")
def stations():
    with sql.connect("Resources/hawaii.sqlite") as con:
        cur = con.cursor()
        cur.execute(f"SELECT station FROM station")
        rows = cur.fetchall()
    con.close()
    
    temps = list(np.ravel(rows))
    return jsonify(temps)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    with sql.connect("Resources/hawaii.sqlite") as con:
        cur = con.cursor()
        cur.execute(f"SELECT station, date FROM measurement WHERE station == 'USC00519281' and date >= '{prev_year}'")
        rows = cur.fetchall()
    con.close()
    
    temps = list(np.ravel(rows))
    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
        
    with sql.connect("Resources/hawaii.sqlite") as con:
        
        if not end:
            
            # Perfoming a query for the minimum temperature, the average temperature, 
            # and the maximum temperature for a specified start
            sel = "SELECT MIN(tobs), AVG(tobs), MAX(tobs) FROM measurement WHERE date >= ?"
            
            
            start = dt.datetime.strptime(start, "%m%d%Y")
                        
            cur = con.cursor()
            cur.execute(sel, (start,))
            rows = cur.fetchall()
            
            temps = list(np.ravel(rows))
            return jsonify(temps = temps)
        
        else:
            
            # Perfoming a query for the minimum temperature, the average temperature, 
            # and the maximum temperature for a specified range
            sel = "SELECT MIN(tobs), AVG(tobs), MAX(tobs) FROM measurement WHERE date >= ? AND date <= ?"

            start = dt.datetime.strptime(start, "%m%d%Y")
            end = dt.datetime.strptime(end, "%m%d%Y")
            
            cur = con.cursor()
            cur.execute(sel, (start, end))
            rows = cur.fetchall()
            
    con.close()
            
    temps = list(np.ravel(rows))
    return jsonify(temps = temps) 

# This code runs the Flask application on the local 
# machine at IP address 127.0.0.1 and port 5000, with debugging enabled        
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)