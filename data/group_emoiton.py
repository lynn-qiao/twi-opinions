# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 15:26:18 2020

@author: xqiao
"""


import pandas as pd

filepath1 = "D:/capstone-project/tlkh_emotion.csv"


tlkh = pd.read_csv(filepath1, encoding='latin1')
tlkh=tlkh[tlkh.sentiment != 'surprise']


tlkh.loc[tlkh['sentiment'] == 'neutural', 'sentiment']='neutral'

tlkh.loc[tlkh['sentiment'] == 'worry', 'sentiment']='fear'

tlkh.loc[tlkh['sentiment'] == 'happiness', 'sentiment']='enjoyment'

tlkh.loc[tlkh['sentiment'] == 'sadness', 'sentiment']='sadness'

tlkh.loc[tlkh['sentiment'] == 'love', 'sentiment']='enjoyment'

tlkh.loc[tlkh['sentiment'] == 'fun', 'sentiment']='enjoyment'

tlkh.loc[tlkh['sentiment'] == 'relief', 'sentiment']='enjoyment'

tlkh.loc[tlkh['sentiment'] == 'hate', 'sentiment']='disgust'

tlkh.loc[tlkh['sentiment'] == 'empty', 'sentiment']='neutral'

tlkh.loc[tlkh['sentiment'] == 'enthusiasm', 'sentiment']='enjoyment'

tlkh.loc[tlkh['sentiment'] == 'boredom', 'sentiment']='anger'

tlkh.loc[tlkh['sentiment'] == 'anger', 'sentiment']='anger'


tlkh['sentiment'].value_counts()
tlkh=tlkh.rename(columns={"content": "text"})



filepath2 = "D:/capstone-project/smileannotationsfinal.csv"

smile = pd.read_csv(filepath2, names=['id','text','sentiment'],encoding='latin1')

smile['sentiment'].value_counts()

smile=smile[smile.sentiment != 'surprise']
smile=smile[smile.sentiment != 'nocode']
smile=smile[smile.sentiment != 'not-relevant']



filepath3 = "D:/capstone-project/kagg_emo.csv"

kagg = pd.read_csv(filepath3, names=['id','sentiment','text'],encoding='latin1')

kagg=kagg.iloc[1:]

kagg['sentiment'].value_counts()

kagg.loc[kagg['sentiment'] == 'joy', 'sentiment']='enjoyment'


filepath4 = "D:/capstone-project/Emotion(angry).csv"

whatsapp = pd.read_csv(filepath4, names=['text','sentiment'],encoding='latin1')


"""
combine 4 files
"""


comb=[kagg[['text', 'sentiment']], smile[['text', 'sentiment']],tlkh[['text', 'sentiment']],whatsapp[['text', 'sentiment']]]

result = pd.concat(comb)

result['sentiment'].value_counts()

result.loc[result['sentiment'] == 'happy', 'sentiment']='enjoyment'
result.loc[result['sentiment'] == 'sad', 'sentiment']='sadness'
result.loc[result['sentiment'] == 'angry', 'sentiment']='anger'
result.loc[result['sentiment'] == 'disgust', 'sentiment']='anger'


result=result[result.sentiment != 'sentiment']

import re

def remove_url(txt):
    return " ".join(re.sub('https?://[A-Za-z0-9./]+', "", txt).split())

def remove_mention(txt):
    return " ".join(re.sub(r'@[A-Za-z0-9]+', "", txt).split())

def clean_text(df):
    df['text']=[remove_url(text) for text in df['text']] 
    df['text']=[remove_mention(text) for text in df['text']] 
    return df

cleancombd=clean_text(result)

cleancombd.to_csv (r'D:/capstone-project/websource.csv', index = False, header=True)
