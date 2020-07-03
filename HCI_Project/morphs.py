import pandas as pd
import urllib.request
import matplotlib.pyplot as plt
import re
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

from wordcloud import WordCloud 

import nltk
from nltk.corpus import stopwords

from collections import Counter


def making_word_cloud():
    print("making word cloud starts")

    data = pd.read_csv("./output/comments_result.csv")

    okt = Okt()

    morphs = []

    for sentence in data['document']:
        morphs.append(okt.pos(sentence))

    noun_adj_adv_list=[]
    except_words = ['것', '나', '내', '수', '게', '말', '더', '때', '거', '볼', '또', '꼭', '이', '좀', '그', '왜', '뭐', '임', '점', '편', '안', '알', '애', '저', '난', '듯', '분', '걸']
    
    for sentence in morphs :
        for word, tag in sentence :
            if tag in ['Noun'] :
                if not word in except_words :
                    noun_adj_adv_list.append(word)

    count = Counter(noun_adj_adv_list)

    words = dict(count.most_common(75))
    sorted_morphs = sorted(words.items(), key=lambda t : t[1], reverse=True)
    sorted_morphs = dict(sorted_morphs)

    # font path
    import os
    nanum_font_path = os.getcwd() + "/Nanum/NanumBarunGothicBold.ttf"

    wordcloud = WordCloud(font_path = nanum_font_path, background_color='white',colormap = "Accent_r",
                        width=6000, height=1500).generate_from_frequencies(sorted_morphs)


    plt.imshow(wordcloud)
    plt.axis('off')
    fig = plt.gcf()
    fig.savefig('./output/wordcloud.png', dpi=500)

    print("making word cloud ended")