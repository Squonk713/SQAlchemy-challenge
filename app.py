import numpy as np
import os
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

file_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
db_path = f"sqlite:///{file_dir}/hawaii.sqlite"
print(db_path)
engine = create_engine(db_path)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
print(Base.classes.keys())

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################

app = Flask (__name__)

@app.route("/")
def home(): 
    print("Server received request for 'Home' page...")
    return(
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"Returns a JSON list of dates and precipitation from the dataset.<br/>"
    f"------------------------------------------------------------------------------------------<br/>"
  
    f"/api/v1.0/stations<br/>"
    f"Returns a JSON list of stations from the dataset.<br/>"
    f"------------------------------------------------------------------------------------------<br/>"
    
    f"/api/v1.0/tobs<br/>"
    f"Returns a JSON list of dates and temperatures for the most active station of the past year from the dataset.<br/>"
    f"------------------------------------------------------------------------------------------<br/>"
  
    f"/api/v1.0/yyyy-mm-dd and /api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/>"
    f"Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.<br/>")

@app.route('/api/v1.0/precipitation')
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query
    results = session.query(measurement.date,measurement.prcp).all()
    # Close session
    session.close()
    # Unravel Tuples into list
    precipitation = list(np.ravel(results))
    # print action to terminal
    print("Server received request for 'Precipitation' page...")
    # return list as JSON
    return jsonify(precipitation)

@app.route('/api/v1.0/stations')
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query
    results = session.query(station.station,station.name,station.latitude,station.longitude,station.elevation).all()
    # Close session
    session.close()
    # Unravel Tuples into list
    stations = list(np.ravel(results))
    # print action to terminal
    print("Server received request for 'Stations' page...")
    # return list as JSON
    return jsonify(stations)

@app.route('/api/v1.0/tobs')
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query
    latest_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    last_date = dt.datetime.strptime(latest_date[0], '%Y-%m-%d')
    first_date = dt.date(last_date.year -1, last_date.month, last_date.day)

    results = session.query(measurement.station,measurement.date,measurement.tobs).filter(measurement.date >= first_date).filter(measurement.station == 'USC00519281').all()

    # Close session
    session.close()
    # Unravel Tuples into list
    tobs = list(np.ravel(results))
    # print action to terminal
    print("Server received request for 'Tobs' page...")
    # return list as JSON
    return jsonify(tobs)

@app.route('/api/v1.0/<start>')
def variable_start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).all()
    # Close session
    session.close()
    # Unravel Tuples into list
    variable_start_date = list(np.ravel(results))
    # print action to terminal
    print("Server received request for 'Variable start date' page...")
    # return list as JSON
    return jsonify(variable_start_date)

@app.route('/api/v1.0/<start>/<stop>')
def variable_start_end_date(start,stop):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= stop).all()
    # Close session
    session.close()
    # Unravel Tuples into list
    variable_start_end_date = list(np.ravel(results))
    # print action to terminal
    print("Server received request for 'Variable start and end date' page...")
    # return list as JSON
    return jsonify(variable_start_end_date)

if __name__ == "__main__":
 app.run(debug=True)