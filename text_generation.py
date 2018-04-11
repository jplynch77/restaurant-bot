import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import keras
import random
from keras.models import load_model

def clean_text(text):
    """Keep only very specific characters"""
    keep_characters = [' ', '!', ',', '.', ':', ';', '?', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                       'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
                       'x', 'y', 'z']

    for char in text:
        if char not in keep_characters:
            text = text.replace(char, ' ')
    return text

def window_transform_text(text, window_size, step_size):
    """Create input output character pairs"""

    # containers for input/output pairs
    text_iterator = range(len(text))[0::step_size]

    inputs = []
    outputs = []
    for i in text_iterator:
        if i + window_size < len(text):
            inputs.append(text[i:(i+window_size)])
            outputs.append(text[i+window_size])

    return inputs, outputs

def encode_io_pairs(text, window_size, step_size):
    """1-Hot encoding of input/output pairs"""

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

def predict_next_chars(model, input_chars, num_to_predict):
    """Do actual character level prediction"""

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

# Read in review data
review_df = pd.read_pickle('data/review_df.pickle')
sample1 = review_df['review'].iloc[0]
sample2 = review_df['review'].iloc[1]

# Get text as one giant text file
corpus = ""
for review in review_df['review']:
    corpus = corpus + review

length_corpus = len(corpus)
unqiue_corpus_chars = set(corpus)

# Clean text
clean_corpus = clean_text(corpus.lower())
chars = sorted(list(set(clean_corpus)))
clean_corpus = clean_corpus.replace('  ',' ')
text = clean_corpus


# This dictionary is a function mapping each unique character to a unique integer
chars_to_indices = dict((c, i) for i, c in enumerate(chars))

# This dictionary is a function mapping each unique integer back to a unique character
indices_to_chars = dict((i, c) for i, c in enumerate(chars))

window_size = 100
step_size = 5
inputs, outputs = window_transform_text(text, window_size, step_size)

window_size = 100
step_size = 5
X, y = encode_io_pairs(text, window_size, step_size)

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

# save model weights
model.save_weights('model_weights/small_model_weights_20180411.hdf5')

start_inds = [0,1,2,4]
for s in start_inds:
    start_index = s
    input_chars = text[start_index: start_index + window_size]

    # use the prediction function
    predict_input = predict_next_chars(model, input_chars, num_to_predict = 100)

    # print out input characters
    print('------------------')
    input_line = 'input chars = ' + '\n' +  input_chars + '"' + '\n'
    print(input_line)
    # print out predicted characters
    line = 'predicted chars = ' + '\n' +  predict_input + '"' + '\n'
    print(line)







