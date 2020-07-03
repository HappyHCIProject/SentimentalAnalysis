import pandas as pd
import urllib.request
import matplotlib.pyplot as plt
import re
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import pickle


def input_processor():
    print("start input data processor")

    comments = pd.read_csv("./output/comments.csv")

    comments = comments.drop(comments.columns[[0]], axis='columns')
    comments.drop_duplicates(subset = ['document'], inplace=True)
    comments['document'] = comments['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
    comments['document'].replace('', np.nan, inplace=True)
    comments = comments.dropna(how='any')
    # print('전처리 후 테스트용 샘플의 개수 :',len(comments))

    stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
    okt = Okt()

    comments_X = []
    for sentence in comments['document']:
        temp_X = []
        temp_X = okt.morphs(sentence, stem=True) # 토큰화
        temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
        comments_X.append(temp_X)

    tokenizer = Tokenizer()

    with open('./output/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle) 

    comments_X = tokenizer.texts_to_sequences(comments_X)
    #print(comments_X)


    drop_comments = [index for index, sentence in enumerate(comments_X) if len(sentence) < 1]

    comments = comments.drop(comments.index[drop_comments])
    comments_X = np.delete(comments_X, drop_comments, axis=0)

    max_len = 30
    comments_X = pad_sequences(comments_X, maxlen = max_len)

    loaded_model1 = load_model('/home/jeongwu/HCI/HCI_Project/output/best_model.h5')
    predict = loaded_model1.predict(comments_X)

    comments_result = comments
    comments_result["predicted_label"] = predict

    comments_result.to_csv("./output/comments_result.csv", encoding="utf-8-sig")

    print("input data processor ended")