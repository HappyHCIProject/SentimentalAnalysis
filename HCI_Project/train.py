import pandas as pd
import urllib.request
import matplotlib.pyplot as plt
import re
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

train_data = pd.read_table('./Movie_rating_data/ratings_train.txt') # train data 
test_data = pd.read_table('./Movie_rating_data/ratings_test.txt') # test data

train_data.drop_duplicates(subset=['document'], inplace=True) # remove duplicated data from column 'document' of train data
train_data = train_data.dropna(how = 'any') # remove rows which is na valued
train_data['document'] = train_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","") # remove data which is not writed by Korean
train_data['document'].replace('', np.nan, inplace=True)
train_data = train_data.dropna(how = 'any')

test_data.drop_duplicates(subset = ['document'], inplace=True) # remove duplicated data from column 'document' of test data
test_data['document'] = test_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","") # regular expression
test_data['document'].replace('', np.nan, inplace=True) # replace blank as NULL
test_data = test_data.dropna(how='any') # remove NULL

stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

okt = Okt()

X_train = []
for sentence in train_data['document']:
    temp_X = []
    temp_X = okt.morphs(sentence, stem=True) # 토큰화
    temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
    X_train.append(temp_X)

X_test = []
for sentence in test_data['document']:
    temp_X = []
    temp_X = okt.morphs(sentence, stem=True) # 토큰화
    temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
    X_test.append(temp_X)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train)

threshold = 3
total_cnt = len(tokenizer.word_index) # number of words
rare_cnt = 0 # count number of words which is shown less than threshold
total_freq = 0 # sum of frequency of words from train data
rare_freq = 0 # sum of frequency of words which is show less than threshold

# key : word, value : frequency
for key, value in tokenizer.word_counts.items():
    total_freq = total_freq + value

    # if frequency is less than threshold, 
    if(value < threshold):
        rare_cnt = rare_cnt + 1
        rare_freq = rare_freq + value

vocab_size = total_cnt - rare_cnt + 1

tokenizer = Tokenizer(vocab_size) 
tokenizer.fit_on_texts(X_train)

with open('./output/tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

X_train = tokenizer.texts_to_sequences(X_train)
X_test = tokenizer.texts_to_sequences(X_test)

y_train = np.array(train_data['label'])
y_test = np.array(test_data['label'])

drop_train = [index for index, sentence in enumerate(X_train) if len(sentence) < 1]
drop_test = [index for index, sentence in enumerate(X_test) if len(sentence) < 1]

X_train = np.delete(X_train, drop_train, axis=0)
y_train = np.delete(y_train, drop_train, axis=0)

X_test = np.delete(X_test, drop_test, axis=0)
y_test = np.delete(y_test, drop_test, axis=0)

def below_threshold_len(max_len, nested_list):
  cnt = 0
  for s in nested_list:
    if(len(s) <= max_len):
        cnt = cnt + 1

max_len = 30

X_train = pad_sequences(X_train, maxlen = max_len)
X_test = pad_sequences(X_test, maxlen = max_len)

from tensorflow.keras.layers import Embedding, Dense, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

model = Sequential()
model.add(Embedding(vocab_size, 100))  # dimension of embedding vector = 100
model.add(LSTM(128)) # LSTM
model.add(Dense(1, activation='sigmoid')) # sigmoid for activation function

# early stopping for preventing overfitting
es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4) 
# save model by using model check point if only it is better than previous one
mc = ModelCheckpoint('./output/best_model.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)

model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
# model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
# epoch = 15, validation data = 20% of train data
history = model.fit(X_train, y_train, epochs=15, callbacks=[es, mc], batch_size=60, validation_split=0.2)

loaded_model = load_model('./output/best_model.h5')
print("\n 테스트 정확도: %.4f" % (loaded_model.evaluate(X_test, y_test)[1]))