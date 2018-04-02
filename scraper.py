import requests
import pandas as pd
from pandas.io.json import json_normalize
import pickle
import re
from bs4 import BeautifulSoup

def url_scraper(url):
    r = requests.get(url)
    json_data = r.json()['data']
    df = json_normalize(json_data)
    return df

def url_generator(city, lat, lng, offset, limit):
    url = 'https://www.theinfatuation.com/api/v1/venues/search?lat=' + str(lat) + '&lng=' + str(lng) + '&city=' + city + '&view_distance=305849.5707222307&sort_order=Highest%20Rated&category%5B%5D=RESTAURANT&offset=' + str(offset) + '&limit=' + str(limit)
    return url

def city_scraper(city_name):
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
    # list(range(0, max_num, 500))
    for offset in range(0, max_num, 500):
        url = url_generator(city, lat, lng, offset=offset, limit=500)
        df = url_scraper(url)
        df_list.append(df)

    final_df = pd.concat(df_list)
    return final_df

# df_list = []
# for name in city_names:
#     df = city_scraper(name)
#     df_list.append(df)

# final_df = pd.concat(df_list)
# final_df.to_pickle('all_city_data.pickle')

df['post.review_link']
base_url = 'https://www.theinfatuation.com'
test = base_url + df['post.review_link'].iloc[0]

r = requests.get(test)
soup = BeautifulSoup(r.content, 'html.parser')

