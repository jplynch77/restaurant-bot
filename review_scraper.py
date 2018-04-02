import requests
import pandas as pd
from pandas.io.json import json_normalize
import pickle
import re
from bs4 import BeautifulSoup
import logging

df = pd.read_pickle('all_city_data.pickle')
base_url = 'https://www.theinfatuation.com'

headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}

logging.basicConfig(filename='review_scaper.log',level=logging.WARNING)

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

with open('review_response_list.pickle', 'wb') as f:
    pickle.dump(response_list, f)
