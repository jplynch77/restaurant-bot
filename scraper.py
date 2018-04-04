import requests
import pandas as pd
from pandas.io.json import json_normalize
import pickle
import re
from bs4 import BeautifulSoup
import logging

def url_scraper(url):
    """Grabs and normalizes json response"""
    r = requests.get(url)
    json_data = r.json()['data']
    df = json_normalize(json_data)
    return df

def url_generator(city, lat, lng, offset, limit):
    """Generates urls to be scraped with different cities, latitudes, and longitudes"""
    url = 'https://www.theinfatuation.com/api/v1/venues/search?lat=' + str(lat) + '&lng=' + str(lng) + '&city=' + city + '&view_distance=305849.5707222307&sort_order=Highest%20Rated&category%5B%5D=RESTAURANT&offset=' + str(offset) + '&limit=' + str(limit)
    return url

def city_scraper(city_name, city_df):
    """Grabs data for each city"""
    subset_df = city_df[city_df['city.slug'] == city_name]

    lat = subset_df['city.map_center.coordinates'].values[0][1]
    lng = subset_df['city.map_center.coordinates'].values[0][0]

    if city_name == 'washington-dc':
        city = 'Washington%20DC'
    else:
        city = city_name.title().replace('-', '%20')

    url = url_generator(city, lat, lng, offset=0, limit=40)

    r = requests.get(url)
    max_num = r.json()['totalCount']

    df_list = []
    for offset in range(0, max_num, 500):
        url = url_generator(city, lat, lng, offset=offset, limit=500)
        df = url_scraper(url)
        df_list.append(df)

    final_df = pd.concat(df_list)
    return final_df

def review_scraper(data_df):
    """Downloads reviews from the links in the infatuation restuarant data"""

    logging.basicConfig(filename='review_scaper.log',level=logging.WARNING)

    base_url = 'https://www.theinfatuation.com'
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}

    response_list = []
    for i, url in enumerate(df['post.review_link']):
        complete_url = base_url + url
        if i % 50 == 0:
            print(i, url)
        try:
            r = requests.get(complete_url, headers=headers)
            response_list.append(r)
        except:
            logging.exception('Failed to download review')

if __name__ == '__main__':
    # Read in city data
    city_df = pd.read_pickle('data/city_df.pickle')
    city_names = city_df['city.name']


    # Downlaod data on individual cities
    df_list = []
    for name in city_names:
        df = city_scraper(name, city_df)
        df_list.append(df)

    data_df = pd.concat(df_list)
    # data_df.to_pickle('all_city_data.pickle')
    data_df = pd.read_pickle('data/all_city_data.pickle')

    # Run review scraper and dump raw response data to a pickle file
    response_list = review_scraper(data_df)
    with open('review_response_list.pickle', 'wb') as f:
        pickle.dump(response_list, f)

