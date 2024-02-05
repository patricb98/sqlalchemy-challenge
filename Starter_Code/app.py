# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"precipitation data for the last year: /api/v1.0/precipitation<br/>"
        f"list of all stations: /api/v1.0/stations<br/>"
        f"list of the previous years temperature data for the most activate station: /api/v1.0/tobs<br/>"
        f"min, max and av temp from given start date(yyyy-mm-dd): /api/v1.0/<start><br/>"
        f"min, max and av temp from given start(yyyy-mm-dd) and end date (yyy-mm-dd):/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation data for the last year"""
    # Query
    query = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()

    session.close()

    # Create a dictionary from the row data and append to a list
    prcp_data = []
    for date, prcp in query:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query
    query = session.query(Station.station, Station.name).all()

    session.close()

    # Create a dictionary from the row data and append to a list
    station_names = []
    for station, name in query:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_names.append(station_dict)

    return jsonify(station_names)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of the previous years temperature data for the most activate station"""
    # Query
    query = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date.between('2016-08-23', '2017-08-23')).\
    filter(Measurement.station == 'USC00519281').all()

    session.close()

    # Create a dictionary from the row data and append to a list
    tobs_data = []
    for date, tobs in query:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the min, max and av temp from given start date to end of dataset"""
    # Query
    query = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    session.close()

    # Create a dictionary from the row data and append to a list
    start_data = []
    for min, max, avg in query:
        start_dict = {}
        start_dict["min"] = min
        start_dict["max"] = max
        start_dict["avg"] = avg
        start_data.append(start_dict)

    return jsonify(start_data)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the min, max and av temp from given start date to end of dataset"""
    # Query
    query = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date.between(start, end)).all()
    

    session.close()

    # Create a dictionary from the row data and append to a list
    start_end_data = []
    for min, max, avg in query:
        start_end_dict = {}
        start_end_dict["min"] = min
        start_end_dict["max"] = max
        start_end_dict["avg"] = avg
        start_end_data.append(start_end_dict)

    return jsonify(start_end_data)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
