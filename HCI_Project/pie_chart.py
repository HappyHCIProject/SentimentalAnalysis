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

def making_pie_chart():
    print("making pie chart starts")

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

    group_colors = ['lightskyblue', 'lightcoral']
    size_val = pos_neg_result['predicted_label'].value_counts()
    size_val
    pie_chart = size_val.plot(kind = 'pie', autopct='%.2f%%', colors=group_colors, title="Positive/Negative Youtube Comments Distribution")

    pie_chart.figure.savefig('./output/pie_chart.png', dpi=500)

    print("making pie chart ended")