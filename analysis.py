df = pd.read_pickle('data/all_city_data.pickle')
review_df = pd.read_pickle('data/review_df.pickle')

# Who has written the most reviews?
review_df.groupby(['author']).count().sort_values('url', ascending=False)

def create_tag_df():
    tag_list = []
    for i in df['post.perfectFor']:
        tag_list.append(json_normalize(i))
    temp = pd.concat(tag_list)
    unique_tags = temp.drop_duplicates()

    tag_df = pd.DataFrame(columns = unique_perfect_for['slug'])
    tag_df['post.review_link'] = np.NaN

    for index, row in df.iterrows():
        tag_df.at[index, 'post.review_link'] = row['post.review_link']
        for tag in row['post.perfectFor']:
            col = tag['slug']

            df_test.at[index, col] = 1

    tag_df = tag_df.fillna(0)
    tag_df.to_pickle('data/tags_df.pickle')

    return tag_df


def create_hours_df():
    hours_df = pd.DataFrame(columns = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
                                    'Friday', 'Saturday'])
    for index, row in df.iterrows():
        hours_df.at[index, 'post.review_link'] = row['post.review_link']
        for tag in row['hours']:
            col = tag['name']

            hours_df.at[index, col] = tag['segments']

    hours_df.to_pickle('data/hours_df.pickle')

    return hours_df

def create_cuisine_df():
    cuisine_list = []
    for i in df['post.cuisine']:
        cuisine_list.append(json_normalize(i))
    temp = pd.concat(cuisine_list)
    cuisine_unique = temp.drop_duplicates()

    cuisine_df = pd.DataFrame(columns = cuisine_unique['slug'])
    cuisine_df['post.review_link'] = np.NaN
    for index, row in df.iterrows():
        cuisine_df.at[index, 'post.review_link'] = row['post.review_link']
        for tag in row['post.cuisine']:
            col = tag['slug']

            cuisine_df.at[index, col] = 1

    cuisine_df = cuisine_df.fillna(0)
    cuisine_df.to_pickle('data/cuisine_df.pickle')

    return cuisine_df

cuisine_df.loc[:, cuisine_df.columns != 'post.review_link'].sum().sort_values(ascending=False)

from sqlalchemy import create_engine
engine = create_engine('postgresql://jplynch:@localhost:5432/restaurant_db')
cuisine_df.to_sql('cuisine', engine, index=False, if_exists='replace')
hours_df.to_sql('hours', engine, index=False, if_exists='replace')
tag_df.to_sql('tags', engine, index=False, if_exists='replace')

df = df.drop(['post.cuisine', 'post.perfectFor', 'hours'], axis=1)
df.to_sql('restuarants', engine, index=False, if_exists='replace')







