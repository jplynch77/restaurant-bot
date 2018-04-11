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


#######################################
# Word and vectorizer analysis
#######################################

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

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

#######################################
# Text generator
#######################################

review_df = pd.read_pickle('data/review_df.pickle')
sample1 = review_df['review'].iloc[0]
sample2 = review_df['review'].iloc[1]

corpus = ""
for review in review_df['review']:
    corpus = corpus + review

len(corpus)
set(corpus)

def cleaned_text(text):
    keep_characters = [' ', '!', ',', '.', ':', ';', '?', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                       'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
                       'x', 'y', 'z']

    for char in text:
        if char not in keep_characters:
            text = text.replace(char, ' ')
    return text

clean_text = cleaned_text(corpus.lower())
text = clean_text.replace('  ',' ')

def window_transform_text(text, window_size, step_size):
    # containers for input/output pairs
    text_iterator = range(len(text))[0::step_size]

    inputs = []
    outputs = []
    for i in text_iterator:
        if i + window_size < len(text):
            inputs.append(text[i:(i+window_size)])
            outputs.append(text[i+window_size])

    return inputs, outputs

window_size = 100
step_size = 5
inputs, outputs = window_transform_text(text, window_size, step_size)

chars = sorted(list(set(text)))


# this dictionary is a function mapping each unique character to a unique integer
chars_to_indices = dict((c, i) for i, c in enumerate(chars))  # map each unique character to unique integer

# this dictionary is a function mapping each unique integer back to a unique character
indices_to_chars = dict((i, c) for i, c in enumerate(chars))  # map each unique integer back to unique character


# transform character-based input/output into equivalent numerical versions
def encode_io_pairs(text,window_size,step_size):
    # number of unique chars
    chars = sorted(list(set(text)))
    num_chars = len(chars)

    # cut up text into character input/output pairs
    inputs, outputs = window_transform_text(text,window_size,step_size)

    # create empty vessels for one-hot encoded input/output
    X = np.zeros((len(inputs), window_size, num_chars), dtype=np.bool)
    y = np.zeros((len(inputs), num_chars), dtype=np.bool)

    # loop over inputs/outputs and tranform and store in X/y
    for i, sentence in enumerate(inputs):
        for t, char in enumerate(sentence):
            X[i, t, chars_to_indices[char]] = 1
        y[i, chars_to_indices[outputs[i]]] = 1

    return X,y

window_size = 100
step_size = 5
X,y = encode_io_pairs(text,window_size,step_size)


from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import keras
import random
from keras.models import load_model


model = Sequential()
model.add(LSTM(200, input_shape=(window_size, len(chars))))
model.add(Dense(len(chars), activation='softmax'))

optimizer = keras.optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)
# compile model --> make sure initialized optimizer and callbacks - as defined above - are used
model.compile(loss='categorical_crossentropy', optimizer=optimizer)

Xsmall = X[:10000,:,:]
ysmall = y[:10000,:]

# train the model
model.fit(Xsmall, ysmall, batch_size=500, epochs=1,verbose = 1)

model.save_weights('model_weights/small_model_weights_20180404.hdf5')

def predict_next_chars(model,input_chars,num_to_predict):
    # create output
    predicted_chars = ''
    for i in range(num_to_predict):
        # convert this round's predicted characters to numerical input
        x_test = np.zeros((1, window_size, len(chars)))
        for t, char in enumerate(input_chars):
            x_test[0, t, chars_to_indices[char]] = 1.

        # make this round's prediction
        test_predict = model.predict(x_test,verbose = 0)[0]

        # translate numerical prediction back to characters
        r = np.argmax(test_predict)                           # predict class of each test input
        d = indices_to_chars[r]

        # update predicted_chars and input
        predicted_chars+=d
        input_chars+=d
        input_chars = input_chars[1:]
    return predicted_chars

start_inds = [0,1,2,4]

for s in start_inds:
    start_index = s
    input_chars = text[start_index: start_index + window_size]

    # use the prediction function
    predict_input = predict_next_chars(model,input_chars,num_to_predict = 100)

    # print out input characters
    print('------------------')
    input_line = 'input chars = ' + '\n' +  input_chars + '"' + '\n'
    print(input_line)

    # print out predicted characters
    line = 'predicted chars = ' + '\n' +  predict_input + '"' + '\n'
    print(line)







