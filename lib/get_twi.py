# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 22:47:51 2020

@author: xqiao
"""

#goal 1: get twitter data 

# import nltk
# from textblob import TextBlob

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



##dont change stuff above

#input: geo,
#standard API cannot trace back more than 1 week

'''
goal 1 get tweet

the Cursor function returns tweets (a searcher) 
iterate through searcher we get tweet object
for tweet object attributes see:https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object

180 Requests/15 mins limit, and per request you can ask for maximum 100 tweets
18,000 tweets/15 mins
'''




def stream_tweets(search_term):
    consumer_key='D4lK7vdhO7c43OwfOsbQDrB97'
    consumer_secret='I1BCFwstQLqr9IosbJFYhSxqVL2y9OXayRLhDqSET9Nkufqp7e'
    access_token='1032764043327627265-H3qdFOtdNnjXIonN9vKugm6bgEql4N'
    access_token_secret='0v3Reluh37JpEZrmd3f0gACqZF28XOFSuCP5nmsCWkOfa'
    auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    api=tweepy.API(auth)
    data = [] # empty list to which tweet_details obj will be added
    counter = 0 # counter to keep track of each iteration
    # for tweet in tweepy.Cursor(api.search, q=search_term, count=100, lang='en', result_type='popular').items(): 
    for tweet in tweepy.Cursor(api.search, wait_on_rate_limit=True, q=search_term, count=100, lang='en', tweet_mode='extended').items(): 
        #okay I cannot search for popularity, fine
        tweet_details = {}
        tweet_details['text'] = tweet.full_text
        # tweet_details['retweets'] = tweet.retweet_count
        # tweet_details['likes']=tweet.favorite_count #why this return 0
        tweet_details['location'] = tweet.user.location
        # tweet_details['followers'] = tweet.user.followers_count
        data.append(tweet_details)
        
        counter += 1
        if counter == 1000: 
            break
        else:
            pass
    return data


# def popular_tweets(search_term):
#     data = [] # empty list to which tweet_details obj will be added
#     for tweet in tweepy.Cursor(api.search, q=search_term, count=100, lang='en', result_type='popular').items(): 
#     # for tweet in tweepy.Cursor(api.search, q=search_term, count=100, lang='en').items(): 
#         #okay I cannot search for popularity, fine
#         tweet_details = {}
#         tweet_details['text'] = tweet.text
#         # tweet_details['retweets'] = tweet.retweet_count
#         # tweet_details['likes']=tweet.favorite_count #why this return 0#
#         tweet_details['location'] = tweet.user.location
#         # tweet_details['followers'] = tweet.user.followers_count
#         data.append(tweet_details)
#     return data


# def neutural_tweets():
#     data = [] # empty list to which tweet_details obj will be added
#     for tweet in tweepy.Cursor(api.search, count=100, lang='en').items(): 
#     # for tweet in tweepy.Cursor(api.search, q=search_term, count=100, lang='en').items(): 
#         #okay I cannot search for popularity, fine
#         tweet_details = {}
#         tweet_details['text'] = tweet.text
#         # tweet_details['retweets'] = tweet.retweet_count
#         # tweet_details['likes']=tweet.favorite_count #why this return 0
#         tweet_details['location'] = tweet.user.location
#         # tweet_details['followers'] = tweet.user.followers_count
#         data.append(tweet_details)
#     return data


"""
stream_tweets(): get recent tweet
counter= total tweets streamed, maxium 18000
for testing purpose, use 1000

popular_tweets(): get popular tweets
"""


"""
goal 2: filter out non-us twitter, label with state abbr

"""    
"""



s2: filter irregular expressions:
    regular place is written in 'city, state' or 'state, country' format
    filter out any len() !=2

s3: filter content & replace with abbr:
    first match [0] with state full name and replace value with state code
    then match [1] with state code
    

"""



def filter_na(df):
    df.loc[:,'location']=df.loc[:,'location'].str.strip()
    df['state']=[re.split(', ',loc) for loc in df.loc[:,'location']] #split location string by comma
    df['len_counter']=[len(item) for item in df.loc[:,'state']] #filter out irregular format
    df_nomissing=df[df.len_counter ==2]
    return df_nomissing


def state_code_finder(row):
    us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'}
    us_state=["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]


    if row['position0'] in us_state_abbrev.keys() and row['position1'] not in us_state:
        key=row['position0']
        return us_state_abbrev[key]
    elif row['position1'] in us_state and row['position0'] not in us_state_abbrev.keys():
        key=row['position1']
        return key
    else:
        return 'nonUS'
    

def filter_non_us(data):
    df=filter_na(data)
    df['position0']=[item[0] for item in df.loc[:,'state']]
    df['position1']=[item[1] for item in df.loc[:,'state']]
    df['state_code'] = None
    df['state_code'] = df.apply (lambda row: state_code_finder(row), axis=1)
    df_us=df[df.state_code !='nonUS']
    return df_us





"""
goal 3: filter url in 'text', filter stop words
"""

def remove_url(txt):
    return " ".join(re.sub('https?://[A-Za-z0-9./]+', "", txt).split())

def remove_mention(txt):
    return " ".join(re.sub(r'@[A-Za-z0-9]+', "", txt).split())

def clean_text(df):
    df.loc[:,'text']=[remove_url(text) for text in df.loc[:,'text']] 
    df.loc[:,'text']=[remove_mention(text) for text in df.loc[:,'text']] 
    return df





"""
wrap it up

"""


def get_covid_tweet(search_term):
    data=pd.DataFrame(stream_tweets(search_term))
    df_us=filter_non_us(data)   
    df_no_url=clean_text(df_us)
    df_no_url=df_no_url.reset_index(drop=True)
    return df_no_url[['text','state_code']]



"""
sentiment analysis

train own dataset
save trained model
Sentiment-LR.pickle 
current accuracy: 79%


"""
import pickle
import os, sys

# path = os.path.abspath(os.path.dirname(sys.argv[0]))
# path1=os.path.join(path,'models', 'Sentiment-SGDClean.pickle')


# file = open(path1, 'rb')
# SGD = pickle.load(file)
# file.close()






# """
# emotion categorization
# """


# path2=os.path.join(path,'models', 'emo_classifier.pickle')

# file = open(path2, 'rb')
# emo_classifier = pickle.load(file)
# file.close()




"""
word cloud

"""
import base64
import io
from wordcloud import WordCloud, STOPWORDS


def get_wordcloud(df):
    texts=df['text'].tolist()
    text=' '.join(texts)
    pil_img = WordCloud(width = 3000, height = 2000, random_state=1, 
                      background_color='salmon', colormap='Pastel1', 
                      collocations=False, stopwords = STOPWORDS).generate(text=text).to_image()
    img = io.BytesIO()
    pil_img.save(img, "PNG")
    img.seek(0)
    img_b64 = base64.b64encode(img.getvalue()).decode()
    return img_b64



"""
plot

"""
import altair as alt

"""
sentiment hist
"""

def sentiment_chart(df_no_url):
    chart=alt.Chart(df_no_url).mark_bar().encode(
        alt.Y("sentiment"),
        alt.X('count()'),
        color=alt.Color('sentiment', legend=None),
    )

    
    text = alt.Chart(df_no_url).mark_text(dx=-30, fontSize=30 , color='white').encode(
        alt.Y("sentiment", title=''),
        alt.X('count()', title='Number of Tweets', axis=alt.Axis(labels=False)),
        text=alt.Text('count()')
    )

    combd=(chart + text).properties(height=250, width=250
    ).configure_axis(grid=False, labelFontSize=20, titleFontSize=20
    ).configure_view(strokeWidth=0)

    return combd

#last 2 remove lines and frames in the background


"""
emotion hist
"""
def emotion_chart(df_no_url):

    emo_chart=alt.Chart(df_no_url).mark_bar().encode(
        alt.Y("emotion", title=''),
        alt.X('count()',title='Number of Tweets', axis=alt.Axis(labels=False)),
        color=alt.Color('emotion', legend=None, scale=alt.Scale(
                domain=['anger', 'sadness','fear','neutral','enjoyment'],
                range=['#f6511d', '#7fb800','#264653','#00a6ed','#ffb400'])),
    )

    
    emo_text = emo_chart.mark_text(align='left', baseline='middle',
                                dx= 3, fontSize=20
    ).encode(text=alt.Text('count()')
    )

    emo_combd=(emo_chart + emo_text).properties(height=250, width=350
    ).configure_axis(grid=False, labelFontSize=15, titleFontSize=20
    ).configure_view(strokeWidth=0)
    return emo_combd

#last 2 remove lines and frames in the background


# if __name__=='__main__':


# data=get_covid_tweet('death')

# data['sentiment']=SGD.predict(data.loc[:,'text'])
# data['emotion']=emo_classifier.predict(data.loc[:,'text'])
# data=data[['sentiment', 'emotion']]
# e_chart=emotion_chart(data)
# e_chart.save('D:/capstone-project/chart1.html')
# e_json=e_chart.to_json()

# data=pd.DataFrame(stream_tweets(search_term))
#     df_us=filter_non_us(data)   
#     df_no_url=clean_text(df_us)
#     df_no_url=df_no_url.reset_index(drop=True)
#     df_no_url['sentiment']=SGD.predict(df_no_url['text'])
#     df_no_url['emotion']=emo_classifier.predict(df_no_url['text'])
#     wordcl=get_wordcloud(df_no_url)
#     s_chart=sentiment_chart(df_no_url)
#     e_chart=emotion_chart(df_no_url)
    
    # e_chart.save('D:/capstone-project/chart1.html')



    
    
