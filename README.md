## SQLAlchemy Challenge

# Files

All files are contained within the 'SurfsUp' folder:
- The analysis and charts for part 1 can be found in the 'climate.ipynb' file.
- The script for part 2 be found in the 'app.py' file.
- The 'Resources' folder contains the SQLite file ('hawaii.sqlite') as well as both tables ('measurements.csv' and 'stations.csv').

# PART 1: SQLAlchemy Exploratory Analysis

For this challenge, SQLAlchemy was used to query and manipulate a SQLite database using python in Jupyter Notebook.

2 tables containing climate data ('measurement' and 'stations') were reflected, and a session created. A series of queries were then performed on preciptation levels and temperature observations with visualisations created.

All data including charts can be found in the climate.ipynb file.

# PART 2: Climate API

The results of the previous analysis were then loaded into an app using Flask to return data in JSON format.

The homepage shows the available routes:

![homepage](https://github.com/ashejaz/sqlalchemy-challenge/assets/127614970/bbc790a0-51d7-43ff-92df-0aa899aeb01a)

The /api/v1.0/precipitation route returns the date and precipitation data as a single dictionary.
Here, 'date' is the key and 'precipitation' is the value.

![prcp](https://github.com/ashejaz/sqlalchemy-challenge/assets/127614970/801f5746-6b1d-431f-a3d0-c6a8855c5be1)

The /api/v1.0/stations route returns a list of all the stations in the database.

![stations](https://github.com/ashejaz/sqlalchemy-challenge/assets/127614970/34159be0-ad7e-4764-add6-4e32e8c275fa)

The /api/v1.0/tobs route returns a list of temperature observations for the last year of the data and for the most active station, USC00519281.

![tobs](https://github.com/ashejaz/sqlalchemy-challenge/assets/127614970/7f38f6fd-a554-4468-a857-94de1b296197)

The /api/v1.0/<start> and /api/v1.0/<start>/<end> are dynamic routes with return maxiumum, average and minimum temperature values based on the date parameters provided (YYYY-MM-DD).

If both a start and end date are provided, the values returned will be for the the start and end date inclusive.

If only a start date is provided, the values returned will be for all dates greater than or equal to the start date.

![summary_stats](https://github.com/ashejaz/sqlalchemy-challenge/assets/127614970/1e838780-2cd3-42ca-ae4f-9e8dcf26ad21)
