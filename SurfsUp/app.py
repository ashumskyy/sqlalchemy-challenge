import datetime as dt
import numpy as np
import os

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
os.chdir(os.path.dirname(os.path.realpath(__file__)))
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine=engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
## WORK NEEDED HERE ##
    return (
        f"<h1>Climate App by Oleksii Shumskyi</h1>"
        f"<h3>Go to: <br><h3>"
        f"<h4><ol><li><a href=http://127.0.0.1:5000/api/v1.0/precipitation>"
        f"Precipitation (/api/v1.0/precipitation)</a></li><br>"
        f"<li><a href=http://127.0.0.1:5000/api/v1.0/stations>"
        f"Stations (/api/v1.0/stations)</a></li><br>"
        f"<li><a href=http://127.0.0.1:5000/api/v1.0/tobs>"
        f"TOBS (/api/v1.0/tobs)</a></li><br>"
        f"<p>'start' and 'end' date should be in the format MMDDYYYY.</p><br>"
        f"<li>http://127.0.0.1:5000/api/v1.0/temp/<start></li></br>"
        f"<li>http://127.0.0.1:5000/api/v1.0/temp/<start>/<end>""</li></ol></h4>"
    )
        # f"<li><a href=http://127.0.0.1:5000/api/v1.0/stations<br/>"
        # f"<li><a href=http://127.0.0.1:5000/api/v1.0/tobs<br/>"
        # f"<li><a href=http://127.0.0.1:5000/api/v1.0/temp/start<br/>"
        # f"<li><a href=http://127.0.0.1:5000/api/v1.0/temp/<start>/<end>"
        # )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    """Return the precipitation data for the last year"""
    # Calculate the date 1 year ago from last date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query for the date and precipitation for the last year
    precipitation_result = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
        
    session.close()
    
    # Dict with date as the key and prcp as the value
    precipitation_dict = {date: prcp for date, prcp in precipitation_result}
    

    return jsonify(precipitation_dict)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    """Return a list of stations."""
    results = session.query(Station.station).all()

    session.close()

    # Unravel results into a 1D array and convert to a list
    stations = list(np.ravel(results))
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def temp_monthly():
    session = Session(engine)

    """Return the temperature observations (tobs) for previous year."""
    # Calculate the date 1 year ago from last date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query the primary station for all tobs from the last year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()

    session.close()
    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))

    # Return the results
    return jsonify(temps=temps)


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    session = Session(engine)

    """Return TMIN, TAVG, TMAX."""

    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        start = dt.datetime.strptime(start, "%m%d%Y")
        # calculate TMIN, TAVG, TMAX for dates greater than start
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
    
        # Unravel results into a 1D array and convert to a list
        temps = list(np.ravel(results))
        return jsonify(temps=temps)

    # calculate TMIN, TAVG, TMAX with start and stop
    ## WORK NEEDED HERE ##
    
    else:
        start = dt.datetime.strptime(start, "%m%d%Y")
        end = dt.datetime.strptime(end, "%m%d%Y")
    
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()

        session.close()

    # Unravel results into a 1D array and convert to a list
        temps = list(np.ravel(results))
        return jsonify(temps=temps)

# This code runs the Flask application on the local machine
# with debugging enable
if __name__ == '__main__':
    app.run(debug=True)

