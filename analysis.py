import requests
import pandas as pd
from pandas.io.json import json_normalize
import pickle
import re
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

with open('review_response_list.pickle', 'rb') as f:
    temp = pickle.load(f)

with open('author_review_dict.pickle', 'rb') as f:
    temp2 = pickle.load(f)

df = pd.read_pickle('all_city_data.pickle')


df = pd.DataFrame(columns = ['url', 'author', 'review'])
for i, elem in enumerate(temp2):
    df.loc[i, 'url'] = list(elem.keys())[0]
    df.loc[i, 'author'] = list(elem.values())[0][0]
    df.loc[i, 'review'] = list(elem.values())[0][1]

df2 = df[df['author'] != '']

# df_train = df.iloc[:4000]
# df_test = df.iloc[4000:]


cv = CountVectorizer(max_features=200)
tv = TfidfVectorizer(max_features=3000)
X = tv.fit_transform(df2['review'])



# Want to classify document by author using logistic regression
# with count vectorizer
le = LabelEncoder()
y = le.fit_transform(df2['author'])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1)

logreg = LogisticRegression(solver='newton-cg', multi_class='multinomial')
logreg.fit(X_train, y_train)

preds = logreg.predict(X_train)
accuracy_score(y_train, preds)

test_preds = logreg.predict(X_test)
accuracy_score(y_test, test_preds)


df2.loc[1, 'review']
df2.groupby(['author']).count().sort_values('url', ascending=False)

list(temp2[0].keys())[0]
list(temp2[0].values())[0][0]
list(temp2[0].values())[1]

dict_list = []
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

    temp_dict = {url : [review_author, review_text]}
    dict_list.append(temp_dict)

# with open('author_review_dict.pickle', 'wb') as f:
#     pickle.dump(dict_list, f)

def get_author_name(body):
    author_tag = 'post__byline__text'
    author_name = soup.find_all('small', {'class' : author_tag})[0].a['href']
    author_name = re.search('[a-z]+-[a-z]+', author_name)[0]

    return author_name




# Can potentially do some machine learning with the
# food rundown images
section_tag = 'post__section'
body = soup.find_all('div', {'class' : section_tag})[0]

# It's going to be easier to just grab all of the html files
def get_main_review(body):
    text_tag = 'post__content__text-block'
    review_html = body.find_all('div', {'class' : text_tag})

    review_text = " ".join([html.text for html in review_html])
    return review_text


body.find_all('div', {'class': 'post__content__dish-block'})[1]

# Get Food Rundown information
def get_food_rundown(rundown_html):
    food_name = body.find_all('div', {'class' : 'post__content__dish-block'})[0].span.text
    food_description = body.find_all('div', {'class': 'post__content__dish-block'})[0].p.text
    img_link = body.find_all('div', {'class' : 'post__content__dish-block'})[0].img['data-src']

    return food_name, food_description, img_link

# Want to create a dataframe of reviews. We can have author






# df = pd.read_pickle('all_city_data.pickle')

df.describe()
df.info()

tag_list = []
for i in df['post.perfectFor']:
    tag_list.append(json_normalize(i))

temp = pd.concat(tag_list)

cuisine_list = []
for i in df['post.cuisine']:
    cuisine_list.append(json_normalize(i))

temp = pd.concat(cuisine_list)
cuisine_array = temp['name'].unique()

df['post.cuisine'].iloc[0]
json_normalize(df['post.cuisine'])
json_normalize(df['post.cuisine'].iloc[0])

cuisine_junction_table

# What should the structure of this table be?
# Separate table with tags as column names?
# Want to be able to easily filter by tag
# Each row corresponds to a restuarant
# Maybe we want to get a list of restaurans that correspond
# to each tag

# Restuarants Table, (primary key restaurat_name)
# Tag Table, (primary key tag_name)
# Junction Table, restuarant name, tag_name

# Cuisine table
# Junction type, restuarant_name cuisine_type

df['post.cuisine']
df['post.review_link']

