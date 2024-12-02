import streamlit as st
from datetime import datetime

from shapely.geometry import Point, Polygon
import geopandas as gpd
import pandas as pd
import geopy

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

import requests

'''
# Taxifare calculator
'''
st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')


st.balloons()

st.sidebar.markdown("# Your next ride !")


d = st.sidebar.date_input(
    "Select the time of the ride",
    value=datetime.today().date()
)

t = st.sidebar.time_input(
    "Select the time of the ride",
    value=datetime.now().time()
)

date_heure = f'{d} {t}'


line_count = st.sidebar.slider('Passenger count', 1, 10, 5)

st.sidebar.markdown("Pickup address")



street = st.sidebar.text_input("Street", "229 West 43rd St")
city = st.sidebar.text_input("City", "New York")
province = st.sidebar.text_input("Province", "New York")
country = st.sidebar.text_input("Country", "United States")

geolocator = Nominatim(user_agent="GTA Lookup")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
location = geolocator.geocode(street+", "+city+", "+province+", "+country)

lat = location.latitude
lon = location.longitude

st.sidebar.markdown("Drop-off address")

street_final = st.sidebar.text_input("Street", "2 Wyckoff Ave")
city_final = st.sidebar.text_input("City", "New York ")
province_final = st.sidebar.text_input("Province", "New York ")
country_final = st.sidebar.text_input("Country", "United States ")

location_final = geolocator.geocode(street_final+", "+city_final+", "+province_final+", "+country_final)
lat_final = location_final.latitude
lon_final = location_final.longitude

map_data = pd.DataFrame({'lat': [lat,lat_final], 'lon': [lon,lon_final]})

st.map(map_data)

'''
## Cash only!
'''

url = 'https://taxifare.lewagon.ai/predict'
params= dict(pickup_datetime=date_heure,
                 pickup_longitude=lon,
                 pickup_latitude=lat,
                 dropoff_longitude=lon_final,
                 dropoff_latitude=lat_final,
                 passenger_count=line_count,
                 )
# data = {"positions":[0,6,7,29]}
r = requests.get(url, params=params)
to_pay=round(r.json()["fare"],2)



# st.write(r.status_code)
st.write("it will cost you:",to_pay, "$")
