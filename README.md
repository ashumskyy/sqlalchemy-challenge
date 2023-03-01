# sqlalchemy-challenge

# In this Module 10 Challenge we had two parts: 

**- Analyze and Explore the Climate Data
**- Design Your Climate App



In Part 1 use Python and SQLAlchemy to do a basic climate analysis and data exploration 
of provided climate database. Specifically, we used SQLAlchemy ORM queries, Pandas, and Matplotlib. 

We started by connecting to SQLite database. Then we used SQLAlchemy automap_base() function to reflect the tables into classes, 
and then saved references to the classes named "station" and "measurement".
After that we linked Python to the database by creating a SQLAlchemy session.

First, we performed a Precipitation Analysis. We found the most recent date in the dataset, 
got the previous 12 months of precipitation data, selected only the "date" and "prcp" values and loaded the query results into a 
Pandas DataFrame. After, we plotted a line chart and printed the summary statistics for the precipitation data.

Then we performed a Station Analysis. We designed a query to calculate the total number of stations in the dataset, created a query
to find the most-active stations, designed a query that calculates the lowest, highest, and average temperatures that filters 
on the most-active station id found in the previous query, and created another query to get the previous 12 months 
of temperature observation (TOBS) data. At last we plotted a histogram with 12 bins (12 months).
At the end we closed our session. 

--------------------------------------------------------------------------------------------------------------------------------------------

In Part 2 we designed a Flask API based on the queries that we just developed. After connecting to our Data Base by using SQLalchemy, 
we created a Homepage where we can see a list of all the available routs. First three are links which led us to:
/api/v1.0/precipitation - a query results from the precipitation analysis,
/api/v1.0/stations - list of stations from the dataset,
/api/v1.0/tobs - a query of the dates and temperature observations of the most-active station for the previous year of data. ('USC00519281').

The last two routs are strings which we copy to the address bar after our local hist address and pass the start date 
or start date and end date.
When we specify the start date, we calculated TempMIN, TempAVG, and TempMAX for all the dates greater than or equal to the start date.
When we specify the start and end date, we calculated TempMIN, TempAVG, and TempMAX for for the dates 
from the start date to the end date, inclusive.



# BONUS! 

**PLEASE NOTICE THAT I ADDED sqlite3app.py FILE WHERE WE USED sqlite3app.py LIBRARY INSTEAD OF SQLALCHEMY. 

