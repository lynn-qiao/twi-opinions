# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 18:45:33 2020

@author: xqiao
"""


"""
load tagged dataset

"""

import pandas as pd

filepath1 = "D:/capstone-project/emotion_sample1.csv"
filepath2 = "D:/capstone-project/emotion_sample2.csv"
filepath3 = "D:/capstone-project/emotion_sample3.csv"
filepath4 = "D:/capstone-project/emotion_sample4.csv"
filepath5 = "D:/capstone-project/emotion_sample5.csv"
filepath6 = "D:/capstone-project/anger_sad_patch.csv"


emotion1 = pd.read_csv(filepath1, encoding='latin1')
emotion2 = pd.read_csv(filepath2, encoding='latin1')
emotion3 = pd.read_csv(filepath3, encoding='latin1')
emotion4 = pd.read_csv(filepath4, encoding='latin1')
emotion5=pd.read_csv(filepath5, encoding='latin1')
emotion6=pd.read_csv(filepath6, encoding='latin1')

emoitons=[emotion1, emotion2, emotion3, emotion4, emotion5, emotion6]

workingset = pd.concat(emoitons)
workingset=workingset.reset_index(drop=True)

workingset.loc[workingset['emotion'] == 'disgust', 'emotion']='anger'
workingset['emotion'].value_counts()


"""
create mask data
"""

def masking(text):
    text=text.lower()
    masking_list=['excited','relief', 'joy', 'proud', 'panic', 'desperate','dread', 'anxiety', 
              'fury','frustrated','annoyed','bitterness','sorrow','grief','misery','discouraged',
              'dislike', 'loathing', 'repugnant', 'averse', 'depressed', 'depression', 'upset',
              'heartbroken', 'hopeless','sorry','unhappy','sad','bereaved','despair','angry',
              'disgust','hostile','upset','pissed','grouchy','hate','cringe','disapprove','enmity']
    for mask in masking_list:
        text=text.replace(mask, '')
    return text
    
def mask_data(df):
    df['text']=[masking(text) for text in df['text']]
    return df


anger=workingset[workingset.emotion == 'anger']
mask_anger=anger.sample(frac=0.6, random_state=100)
nomask_anger=anger.drop(mask_anger.index)
mask_anger=mask_data(mask_anger)

enjoy=workingset[workingset.emotion == 'enjoyment']
mask_enjoy=enjoy.sample(frac=0.6, random_state=100)
nomask_enjoy=enjoy.drop(mask_enjoy.index)
mask_enjoy=mask_data(mask_enjoy)

sad=workingset[workingset.emotion == 'sadness']
mask_sad=sad.sample(frac=0.6, random_state=100)
nomask_sad=sad.drop(mask_sad.index)
mask_sad=mask_data(mask_sad)

fear=workingset[workingset.emotion == 'fear']
mask_fear=fear.sample(frac=0.6, random_state=100)
nomask_fear=fear.drop(mask_fear.index)
mask_fear=mask_data(mask_fear)



"""
training1: mix all
training2: train on no mask, test on mask


"""

training1=[mask_anger,  mask_fear, mask_enjoy, mask_sad,
           nomask_anger,  nomask_enjoy, nomask_fear, nomask_sad]

workingset1 = pd.concat(training1)
workingset1=workingset1.reset_index(drop=True)



"""
some data cleaning
clean comma, period and one-word post?

"""
import re
import string

def remove_punct(text):
    text  = "".join([char for char in text if char not in string.punctuation])
    text = re.sub('[0-9]+', '', text)
    return text


workingset1['text'] = workingset1['text'].apply(lambda x: remove_punct(x))
workingset1['count']=workingset1['text'].apply(lambda x : len(x.split()))

workingset2=workingset1[workingset1['count'] > 3]

workingset2=workingset2[['text', 'emotion']]
workingset2.to_csv (r'D:/capstone-project/localsource.csv', index = False, header=True)


"""
training

"""
import pandas as pd
import numpy as np

filepath1='D:/capstone-project/localsource.csv'
filepath2='D:/capstone-project/websource.csv'

local=pd.read_csv(filepath1, encoding='latin1')
web=pd.read_csv(filepath2, encoding='latin1')
web=web.rename(columns={"sentiment": "emotion"})
web['text']=web['text'].apply(lambda x: np.str_(x))


def remove_url(txt):
    return " ".join(re.sub('https?://[A-Za-z0-9./]+', "", txt).split())

def remove_mention(txt):
    return " ".join(re.sub(r'@[A-Za-z0-9]+', "", txt).split())

def clean_text(df):
    df['text']=[remove_url(text) for text in df['text']] 
    df['text']=[remove_mention(text) for text in df['text']] 
    return df



web=clean_text(web)

together=[local, web]

data=pd.concat(together)
data['emotion'].value_counts()

"""
lemmanization
"""

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
# nlp = spacy.load('en_core_web_sm')

# def tokenize_lemma(text):
#     return [w.lemma_.lower() for w in nlp(text)]

# stop_words_lemma = set(tokenize_lemma(' '.join(STOP_WORDS)))


"""
training

"""



train=data.sample(frac=0.8,random_state=200) #random state is a seed value
X_train=train['text']
y_train=train['emotion']
test=data.drop(train.index)
X_test=test['text']
y_test=test['emotion']



from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV



sgd_pipe = Pipeline([('vectorizer', TfidfVectorizer(ngram_range=(1,2),
                                                    # max_df=1, 
                                                    min_df=5,
                                                    stop_words=STOP_WORDS.union({'ll', 've','covid','virus','coronavirus'}),
                                                    )), 
                     ('clf', SGDClassifier(max_iter=1000))])

parameters = {
    'vectorizer__max_df':(0.75, 0.8, 1.0),
    'clf__alpha': (0.0002, 0.0001, 0.00001),
}

grid = GridSearchCV(sgd_pipe, parameters, cv=10)
grid.fit(X_train,y_train)

grid.score(X_train,y_train)

grid.score(X_test, y_test)


grid.best_params_

import pickle

file = open('D:/capstone-project/emo_classifier.pickle','wb')
pickle.dump(grid, file)
file.close()