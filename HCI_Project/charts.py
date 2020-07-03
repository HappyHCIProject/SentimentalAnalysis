import pandas as pd
import urllib.request
import matplotlib.pyplot as plt
import re
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from matplotlib import font_manager, rc
from matplotlib import style
from collections import Counter
import operator

def making_charts():
    print("making charts starts")

    result = pd.read_csv("./output/comments_result.csv")
    result = result.drop(result.columns[[0]], axis='columns')

    sorted_result = result.sort_values(by=['predicted_label'], axis = 0)

    pos_neg_result = sorted_result
    pos_neg_result['predicted_label'] = (sorted_result['predicted_label'] > 0.5).astype(int)
    pos_neg_result['predicted_label'] = pos_neg_result['predicted_label'].apply(str)

    pos_neg_result.loc[pos_neg_result['predicted_label'] == '1', 'predicted_label'] = 'Positive'
    pos_neg_result.loc[pos_neg_result['predicted_label'] == '0', 'predicted_label'] = 'Negative'

    font_name = font_manager.FontProperties(fname="/home/jeongwu/HCI/HCI_Project/Nanum/NanumBarunGothicBold.ttf").get_name()
    rc('font', family=font_name)
    style.use('ggplot')

    pos_result = pos_neg_result[pos_neg_result['predicted_label'] == 'Positive']
    neg_result = pos_neg_result[pos_neg_result['predicted_label'] == 'Negative']

    okt = Okt()

    pos_morphs = []

    for sentence in pos_result['document']:
        pos_morphs.append(okt.pos(sentence))

    pos_noun_list=[]
    except_words = ['것', '나', '내', '수', '게', '말', '더', '때', '거', '볼', '또', '꼭', '이', '좀', '그', '왜', '뭐', '임', '점', '편', '안', '알', '애', '저', '난', '듯', '분', '걸']
        
    for sentence in pos_morphs :
        for word, tag in sentence :
            if tag in ['Noun'] :
                if not word in except_words :
                    pos_noun_list.append(word)

    pos_count = Counter(pos_noun_list)
    pos_words = dict(pos_count.most_common(5))

    neg_morphs = []

    for sentence in neg_result['document']:
        neg_morphs.append(okt.pos(sentence))

    neg_noun_list=[]
    except_words = ['것', '나', '내', '수', '게', '말', '더', '때', '거', '볼', '또', '꼭', '이', '좀', '그', '왜', '뭐', '임', '점', '편', '안', '알', '애', '저', '난', '듯', '분', '걸']
        
    for sentence in neg_morphs :
        for word, tag in sentence :
            if tag in ['Noun'] :
                if not word in except_words :
                    neg_noun_list.append(word)

    neg_count = Counter(neg_noun_list)
    neg_words = dict(neg_count.most_common(5))

    pos_words = dict(pos_words)
    pos_words= sorted(pos_words.items(), key=operator.itemgetter(1), reverse = True)

    neg_words = dict(neg_words)
    neg_words= sorted(neg_words.items(), key=operator.itemgetter(1), reverse = True)

    pos_x = [pos_words[0][1], pos_words[1][1], pos_words[2][1], pos_words[3][1], pos_words[4][1]]
    neg_x = [neg_words[0][1], neg_words[1][1], neg_words[2][1], neg_words[3][1], neg_words[4][1]]

    pos_y = [pos_words[0][0], pos_words[1][0], pos_words[2][0], pos_words[3][0], pos_words[4][0]]
    neg_y = [neg_words[0][0], neg_words[1][0], neg_words[2][0], neg_words[3][0], neg_words[4][0]]

    fig, axes = plt.subplots(nrows=2, sharey=False)
    plt.title('긍정/부정 키워드 Top 5', position=(0.5, 2.25))
    plt.figure(figsize=(8, 8))

    axes[0].barh(pos_y, pos_x, align='center', color='dodgerblue')
    axes[1].barh(neg_y, neg_x, align='center', color='coral')
    axes[0].set_ylabel('긍정 키워드')
    axes[1].set_ylabel('부정 키워드')
    plt.show()

    fig.savefig('./output/keywords.png', dpi=500, bbox_inches = "tight")

    sorted_result = result.sort_values(by=['predicted_label'], axis = 0)
    sorted_result['predicted_label'] = sorted_result['predicted_label'].round(2)

    result_for_all = sorted_result
    result_for_all['quantity'] = 1

    result_for_all = result_for_all.groupby('predicted_label').sum()

    line = plt.figure()
    plt.title('전체 댓글 감정 지수 분포도')

    plt.plot(result_for_all, color='slateblue')

    line.savefig('./output/line.png', dpi=500, bbox_inches = "tight")

    print("making charts ended")