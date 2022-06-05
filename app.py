import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# set up our database engine for the Flask application
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect the database into our classes
Base = automap_base()

# reflect our tables
Base.prepare(engine, reflect=True)

# save our references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database 
session = Session(engine)

# Set Up Flask
app = Flask(__name__)

# define the welcome route
#The foward slash denotates tht we we want to put our data at the root of our routes
@app.route("/")

# add the routing information for each of the other routes
# add the precipitation, stations, tobs, and temp routes
def welcome():
    return(
     '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# Precipitation Route
@app.route("/api/v1.0/precipitation")

# create the precipitation() function
# add the line of code that calculates the date one year ago from the most recent date in the database
# write a query to get the date and precipitation for the previous year
# create a dictionary with the date as the key and the precipitation as the value. 
# To do this, we will "jsonify" our dictionary. Jsonify() is a function that converts the dictionary to a JSON file
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)


# Stations Route
# return a list of all the stations
# defining the route and route name
@app.route("/api/v1.0/stations")

# create a new function called stations()
# create a query that will allow us to get all of the stations in our database
# unraveling our results into a one-dimensional array.
# convert our unraveled results into a list
# we'll jsonify the list and return it as JSON
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)


# Monthly Temperature Route
# return the temperature observations for the previous year
# defining the route
@app.route("/api/v1.0/tobs")

# create a function called temp_monthly()
# calculate the date one year ago from the last date in the database
# query the primary station for all the temperature observations from the previous year
# unravel the results into a one-dimensional array and convert that array into a list. Then jsonify the list and return our results
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results)) 
    return jsonify(temps=temps)   


# Statistics Route
# provide both a starting and ending date
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# create a function called stats()
# add parameters to our stats()function: a start parameter and an end parameter. For now, set them both to None
# create a query to select the minimum, average, and maximum temperatures from our SQLite database
# query our database using the list that we just made. Then, we'll unravel the results into a one-dimensional array and convert them to a list
# take note of the asterisk in the query next to the sel list. Here the asterisk is used to indicate there will be multiple results for our query: minimum, average, and maximum temperatures.
# calculate the temperature minimum, average, and maximum with the start and end dates. We'll use the sel list, which is simply the data points we need to collect. 
# Let's create our next query, which will get our statistics data
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
