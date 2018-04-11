import requests
import pandas as pd
from pandas.io.json import json_normalize
import pickle
import re
from bs4 import BeautifulSoup

def get_author_name(body):
    author_tag = 'post__byline__text'
    author_name = soup.find_all('small', {'class' : author_tag})[0].a['href']
    author_name = re.search('[a-z]+-[a-z]+', author_name)[0]

    return author_name

def get_main_review(body):
    text_tag = 'post__content__text-block'
    review_html = body.find_all('div', {'class' : text_tag})

    review_text = " ".join([html.text for html in review_html])
    return review_text

def get_food_rundown(rundown_html):
    food_name = body.find_all('div', {'class' : 'post__content__dish-block'})[0].span.text
    food_description = body.find_all('div', {'class': 'post__content__dish-block'})[0].p.text
    img_link = body.find_all('div', {'class' : 'post__content__dish-block'})[0].img['data-src']

    return food_name, food_description, img_link

def reviews_to_df(review_response_list):
    df = pd.DataFrame(columns = ['url', 'author', 'review'])
    for i, review in enumerate(temp):
        soup = BeautifulSoup(review.content, 'html.parser')
        section_tag = 'post__section'
        url = review.url

        try:
            body = soup.find_all('div', {'class' : section_tag})[0]
        except:
            print("Missing body for {0}".format(url))
            continue

        if i % 50 == 0:
            print(i)

        review_text = get_main_review(body)
        try:
            review_author = get_author_name(body)
        except:
            print("Missing author for {0}".format(url))
            review_author = ''

        df.loc[i, 'url'] = url
        df.loc[i, 'author'] = review_author
        df.loc[i, 'review'] = review_text

        return df

with open('data/review_response_list.pickle', 'rb') as f:
    temp = pickle.load(f)

review_df = review_response_list(temp)
# review_df.to_pickle('data/review_df.pickle')


