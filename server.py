from flask import Flask, request, render_template
import tweepy
from tweepy import OAuthHandler
from tweepy import Cursor
import re
import numpy as np
import pandas as pd
import itertools
import collections
from datetime import datetime
import json
from textblob import TextBlob
import pickle
import base64
import io
from wordcloud import WordCloud, STOPWORDS
import altair as alt
import os, sys
import sklearn

from lib.get_twi import get_covid_tweet, get_wordcloud, sentiment_chart, emotion_chart


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result')
def result():
    args = request.args
    keyword = str(args.get('search_term'))
    regex = re.compile('[^a-zA-Z]')
    keyword=regex.sub(' ', keyword)
    search_term='{} (COVID OR COVID-19 OR Coronavirus) -filter:retweets'.format(keyword)
    df=get_covid_tweet(search_term)
    shape=df.shape[0]
    wordcloud=get_wordcloud(df)

    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    path1=os.path.join(path,'lib','models', 'Sentiment-SGDClean.pickle')

    file = open(path1, 'rb')
    SGD = pickle.load(file)
    file.close()

    path2=os.path.join(path,'lib','models', 'emo_classifier.pickle')
    file = open(path2, 'rb')
    emo_classifier = pickle.load(file)
    file.close()
    
    df['sentiment']=SGD.predict(df.loc[:,'text'])
    df['emotion']=emo_classifier.predict(df.loc[:,'text'])
    s_chart=sentiment_chart(df)
    e_chart=emotion_chart(df)
    s_chart_json=s_chart.to_json()
    e_chart_json=e_chart.to_json()


    return render_template('graph.html', shape=shape, s_chart=s_chart_json, e_chart=e_chart_json, img_data=wordcloud)



if __name__=='__main__':
    app.run(debug=True)



    
