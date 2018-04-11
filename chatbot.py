import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import pickle
import re
from sqlalchemy import create_engine
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import googlemaps
from datetime import datetime

gmaps.geocode("Chelsea", components={'administrative_area':"NY"})
gmaps.geocode('Chelsea', components={'locality' : 'Manhattan'})

gmaps.geocode('Chelsea', components={'locality' : 'New York County'})
gmaps.geocode('Chelsea', components={'sublocality' : 'Manhattan'})

gmaps.geocode('Chelsea', components={'sublocality_level_1' : 'Manhattan'})


gmaps.geocode('Chelsea', components={'administrative_area_level_2' : 'New York'})

gmaps.geocode('Chelsea', components={'postal_code' : '10011'})


components = { "administrative_area": "MA" }
gmaps = googlemaps.Client(key='AIzaSyAYALnAdkdCW7zGklrodCK4A7XyTeszy7M')

def bot():
    location = input("Where do you want to eat? ")

    geocode_result = gmaps.geocode(location)
    place = geocode_result[0]['address_components'][0]['short_name']

    print("So you want to eat in " + place)

geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
geocode_result = gmaps.geocode('14th and 6th')
geocode_result = gmaps.geocode('Im looking for restuarant near 14th and 6th')
geocode_result = gmaps.geocode('Flatiron')
geocode_result = gmaps.geocode('Chelsea')
gmaps.geocode('Chelsea NY')
gmaps.geocode('LES')
gmaps.geocode('Broome and Crosby')
gmaps.geocode('Lower East Side')
gmaps.geocode('Brookln Heightz')
gmaps.geocode('Manhattan')
gmaps.geocode('UES')

# Geocoding an address
# Read in zillow neighborhood geodata
gdf = gpd.read_file('data/zillow_nyc.shp')
hood_names = gdf[(gdf['County'] == 'New York') & (gdf['City'] == 'New York')]['Name']
nyc_gdf = gdf[(gdf['County'] == 'New York') & (gdf['City'] == 'New York')]
gdf.head()

# Read in restuarant data with geo coordinates
engine = create_engine('postgresql://jplynch:@localhost:5432/restaurant_db')
df = pd.read_sql_table('restaurants', engine)

# Get latitude and longitude into shapley Point format for Periyali restaurant
temp = df[df['city'] == 'New York'][['name', 'geo_point.coordinates']]
temp[['name', 'geo_point.coordinates']].head()
str_point = temp.iloc[0][1]
lon = float(re.search('^{(.*),', str_point)[1])
lat = float(re.search(',(.*)}$', str_point)[1])
point = Point(lat, lon)

# Get polygon from zillow data for Suffolk, Town of Islip, Bohemia
polygon = gdf['geometry'].iloc[0]
polygon.area
polygon.bounds

# So we use the contains method from the shapley method on a polygon
# object to test whether a certain polygon contains a point
polygon.contains(point)

# Now let's get the right polygon for Periyali, which appears to be in flatiron
gdf.head()
flatiron = gdf[gdf['Name'] == 'Flatiron District']['geometry'].iloc[0]
flatiron.bounds
flatiron.contains(point)

# Okay let's try looping through everything
gdf['geometry'].apply(lambda x: x.contains(point))

home_lat = 40.7391482
home_lon = -73.9985749
home_point = Point(home_lon, home_lat)
chelsea = nyc_gdf[nyc_gdf['Name'] == 'Chelsea']['geometry'].iloc[0]
chelsea.bounds
chelsea.contains(home_point)

# bounds = (minx, miny, maxx, maxy)

point_in_polys = sjoin(point, poly, how='left')
grouped = pointInPolys.groupby('index_right')
list(grouped)

# First thing is to create a neural network that can generate text that is
# similar to existing infaution reviews

# I want a service where I can just text a simple natural
# language description of what I want and the bot will text
# me back the short pithy infatuation description

from twilio.rest import Client
client = Client()

client.messages.create(to="+16302727163",
                       from_="+17083157430",
                       body="Hello from Python!")

# Search message for location
# Search message for type of restuarant
# Search message for any relevant tags
# Search for breakfast, lunch, or dinner.
# Urgency
# Fancy, casual


# Understanding location language is going to be very difficult
# Near 16th and 6th (for example)
# Can get neighborhood information from the review html
# Need to understand very casual location information (UES = upper east side)
#  qq qqq



# Definitely need to have neighborhood information
# Definitely need to just focus on an NYC chatbot at first
# Unless i acquire an enormous more amount of data (yelp)
# this is mostly going to be an exercise in defining custom
# rules

# Bar
# Brunch
# Cafe
# Lunch
# Dinner

# Ideally the ability to clarify questions

cuisine
price_tier

ny_df = df[df['state'] == 'NY']
ny_df.groupby('post.rating').count()

# 583 restuarants don't have real ratings in NY
ny_df.columns
