# %%
from typing import Text
from altair.vegalite.v4.schema.channels import Column
from altair.vegalite.v4.schema.core import Aggregate
import pandas as pd
import altair as alt
import altair_saver
import numpy as np
import time 
from datetime import timedelta

from pandas.core.tools.datetimes import to_datetime
alt.data_transformers.enable("json")
# %%
url = "https://raw.githubusercontent.com/byuidatascience/data4missing/master/data-raw/flights_missing/flights_missing.json"

data = pd.read_json(url)

data.minutes_delayed_total = pd.to_timedelta(data.minutes_delayed_total,"m")
data.minutes_delayed_weather = pd.to_timedelta(data.minutes_delayed_weather,"m")
data['yeardt'] = pd.to_datetime(data.year.fillna(1900).astype('int'), format="%Y")
d = {'January':1, 'February':2, 'March':3, 'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12 }

data['monthnum']  = data.month.map(d).dropna()
data['monthdt'] = pd.to_datetime(data.monthnum,format='%m')
data.info()
# %%
# Which airport has the worst delays? 
# How did you choose to define “worst”? 
# As part of your answer, include a table that
# lists the total 
# number of flights, 
# total number of delayed flights, 
# the proportion of delayed flights, and 
# average delay time, in hours, for each airport.

#MonthNum month as a Number
#MonthName month as a Name
#Year year as  a Number
#Date Datetime of Month and  Year
#NumOfFlights Count of FLights by Month and Year
#NumDelayedFlights Count of Delayed Flights by Month and Yeaar
#DelayTime How much time was Delayed in the Month
#PrevDelayTime Preventable Delay time so Delay Time without
#Weather since you cannot control that. Can Predict,
#But giving them  the benefit of the doubt and making the assumption
#that all weather is unaviodable.


q1_table = pd.DataFrame({'AirportName' : data.airport_name,
'AirportCode' : data.airport_code,
'MonthName' : data.month,
'MonthNum' : data.monthnum, 
'YearNum' : data.year,
'Date' : pd.to_datetime((data.monthnum.dropna().astype('int').astype('string') + '/' + data.year.dropna().astype('int').astype('string')).dropna()),
'NumOfFlights' : data.num_of_flights_total,
'NumDelayedFlights' : data.num_of_delays_total,
'DelayTime' : data.minutes_delayed_total / 60,
'PrevDelayTime' : (data.minutes_delayed_total - data.minutes_delayed_weather)})

q1_table.info()
q1_table.groupby('AirportCode').agg(
    'NumOfFlights'
)
    # %%
