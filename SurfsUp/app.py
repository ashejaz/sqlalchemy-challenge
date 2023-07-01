# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)
# Create our session (link) from Python to the DB
session = Session(engine)

# Define the most recent date in the database
last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
last_date = dt.datetime.strptime(last_date[0], "%Y-%m-%d").date()
# Define the date 1 year before the most recent date
one_year_ago = last_date - dt.timedelta(days=365)

#################################################
# Flask Routes
#################################################
# Define the homepage route
@app.route("/")
def home():
    return (
        f"Welcome to the Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

# Define the precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Query to retrieve the last 12 months of precipitation data
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()
    # Convert the results to a dictionary with date as the key and prcp as the value
    precipitation_dict = dict(precipitation_data)
    return jsonify(precipitation_dict)

# Define the stations route
@app.route("/api/v1.0/stations")
def stations():

    # Perform the query to retrieve the data of all stations
    stations_data = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    
    # Convert the query results to list of dictionaries
    station_list = []
    for station, name, latitude, longitude, elevation in stations_data:
        station_dict = {"station": station, "name": name, "latitude": latitude, "longitude": longitude, "elevation": elevation}
        station_list.append(station_dict)

    return jsonify(station_list)

# Define the temperature observations route
@app.route("/api/v1.0/tobs")
def tobs():

    # Perform the query to retrieve the most active station
    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).\
        first()
    
    # Perform the query to retrieve the temperature observations for the most active station in the last 12 months
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station[0]).\
        filter(Measurement.date >= one_year_ago).all()
    
    # Convert the results to a list of dictionaries
    tobs_list = []
    for date, tobs in tobs_data:
        tobs_dict = {"date": date, "tobs": tobs}
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

# Define the start and start-end route
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats(start, end=None):
    
    # Perform the query to calculate the temperature statistics based on the specified start and end date

    # If no end date provided:
    if end:
        temperature_stats_data = session.query(func.min(Measurement.tobs),
                                               func.avg(Measurement.tobs),
                                               func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
    else:
        # If end date provided:
        temperature_stats_data = session.query(func.min(Measurement.tobs),
                                               func.avg(Measurement.tobs),
                                               func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
    session.close()

    # Convert the results to a dictionary
    temperature_stats_dict = {"TMIN": temperature_stats_data[0][0],
                              "TAVG": temperature_stats_data[0][1],
                              "TMAX": temperature_stats_data[0][2]}

    return jsonify(temperature_stats_dict)

# Close session
session.close()

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)