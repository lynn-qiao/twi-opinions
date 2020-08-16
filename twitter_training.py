# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 17:11:33 2020

@author: xqiao
"""

import pandas as pd

filepath = "D:/capstone-project/2477_4140_bundle_archive/training.1600000.processed.noemoticon.csv"
emotion16 = pd.read_csv(filepath, encoding='latin1')

emotion16.columns=['target', 'ids', 'date', 'flag', 'user','text']

emotion16.loc[emotion16['target'] ==0,'target' ] = 'negative'
emotion16.loc[emotion16['target'] ==2,'target' ] = 'neutural' #actually no neutural
emotion16.loc[emotion16['target'] ==4,'target' ] = 'positive'

#select 2000 neg and 2000 pos for training just to save time

pos=emotion16[emotion16.target == 'positive']
neg=emotion16[emotion16.target == 'negative']

pos2000=pos.sample(n=10000)
neg2000=neg.sample(n=10000)

working=[pos2000, neg2000]

workingset = pd.concat(working)
workingset=emotion16
workingset=workingset.reset_index(drop=True)


train=workingset.sample(frac=0.8,random_state=200) #random state is a seed value
X_train=train['text']
y_train=train['target']
test=workingset.drop(train.index)
X_test=test['text']
y_test=test['target']


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from spacy.lang.en.stop_words import STOP_WORDS
import en_core_web_sm

from sklearn.naive_bayes import MultinomialNB
import re
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV

MultiNB = Pipeline([('vectorizer', TfidfVectorizer()),
                ('clf', MultinomialNB())])

MultiNB.fit(X_train,y_train)
MultiNB.score(X_train,y_train)

from numpy import linspace

params={'clf__alpha': linspace(2, 2.1, 10)}
grid = GridSearchCV(MultiNB, cv=5, param_grid=params)

grid.fit(X_train,y_train)
grid.best_params_

grid.score(X_train,y_train)
grid.score(X_test, y_test)

import pickle

file = open('Sentiment-NB.pickle','wb')
pickle.dump(grid, file)
file.close()

MultiNB.score(X_test,y_test)

#confustion matrix
NB_pred=MultiNB.predict(X_test)
matrix = confusion_matrix(y_test, NB_pred)
label_names = pd.Series(['negative', 'positive'])
pd.DataFrame(matrix,
     columns='Predicted ' + label_names,
     index='Is ' + label_names).div(matrix.sum(axis=1), axis=0)


from sklearn.linear_model import SGDClassifier
sgd_pipe = Pipeline([('vectorizer', TfidfVectorizer()), # lemmatization removed to improve runtime
                     ('clf', SGDClassifier(max_iter=40))])

parameters = {'clf__alpha': (0.001, 0.0001, 0.00001),
              'clf__loss': ('log', 'hinge'), # log = Logistic Regression, hinge = Linear SVM
}

grid = GridSearchCV(sgd_pipe, parameters, cv=5)
grid.fit(X_train,y_train)
grid.fit(X_cltrain, y_train)
grid.score(X_cltrain,y_train)
grid.score(X_cltest, y_test)

import pickle

file = open('Sentiment-SGDClean.pickle','wb')
pickle.dump(grid, file)
file.close()

grid.score(X_train,y_train)
grid.score(X_test, y_test)


SGD.score(X_cltrain,y_train)
SGD_pred=SGD.predict(X_cltest)


matrix = confusion_matrix(y_test, SGD_pred)
label_names = pd.Series(['negative', 'positive'])
pd.DataFrame(matrix,
     columns='Predicted ' + label_names,
     index='Is ' + label_names).div(matrix.sum(axis=1), axis=0)




import pickle

file = open('Sentiment-SGD.pickle','wb')
pickle.dump(grid, file)
file.close()







def remove_url(txt):
    return " ".join(re.sub('https?://[A-Za-z0-9./]+', "", txt).split())

def replace_mention(txt):
    return " ".join(re.sub(r'@[A-Za-z0-9]+', "", txt).split())

def clean_text(X):
    X=[remove_url(text) for text in X] 
    X=[replace_mention(text) for text in X] 
    return X


X_cltrain=clean_text(X_train)
X_cltest=clean_text(X_test)

nlp = en_core_web_sm.load(disable=['parser','tagger','ner','textcat'])
STOP_WORDS = STOP_WORDS.union({'ll', 've'})

def tokenize_lemma(text):
    return [w.lemma_ for w in nlp(text)]

stop_words_lemma = set(w.lemma_ for w in nlp(' '.join(STOP_WORDS)))

est = Pipeline([('vectorizer', TfidfVectorizer(
                                               stop_words=stop_words_lemma,
                                               tokenizer=tokenize_lemma)),
                ('classifier', MultinomialNB())])



est.fit(X_cltrain,y_train) # This may take 2 or 3 minutes to run 
est.score(X_cltest,y_test)


from sklearn.linear_model import SGDClassifier

sgd_pipe = Pipeline([('vectorizer', TfidfVectorizer(ngram_range=(1,2),
                                               stop_words=STOP_WORDS)), # lemmatization removed to improve runtime
                     ('classifier', SGDClassifier(max_iter=40))])


from sklearn.model_selection import GridSearchCV          

parameters = {'vectorizer__ngram_range': [(1, 1), (1, 2)], 
              'classifier__alpha': (0.001, 0.0001, 0.00001),
              'classifier__loss': ('log', 'hinge'), # log = Logistic Regression, hinge = Linear SVM
}

grid = GridSearchCV(sgd_pipe, parameters, cv=5)
grid.fit(X_cltrain,y_train) # This may take 2 or 3 minutes to run 

est = grid.best_estimator_  #  Let's have a closer look at the best parameters...
est.score(X_cltest,y_test) 
y_pred=est.predict(X_cltest)






"""
use pickle to dump/read models



file = open('Sentiment-LR.pickle','wb')
pickle.dump(LRmodel, file)
file.close()


file = open('..path/vectoriser-ngram-(1,2).pickle', 'rb')
    vectoriser = pickle.load(file)
    file.close()

"""