# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 23:06:03 2020

@author: xqiao
"""

"""
Ekman's 5 atlas of emotion
enjoyment, sadness, anger, fear, disgust

"""

import tweepy
from tweepy import OAuthHandler
from tweepy import Cursor

consumer_key='D4lK7vdhO7c43OwfOsbQDrB97'
consumer_secret='I1BCFwstQLqr9IosbJFYhSxqVL2y9OXayRLhDqSET9Nkufqp7e'

access_token='1032764043327627265-H3qdFOtdNnjXIonN9vKugm6bgEql4N'
access_token_secret='0v3Reluh37JpEZrmd3f0gACqZF28XOFSuCP5nmsCWkOfa'

auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api=tweepy.API(auth)

def stream_tweets(search_term):
    data = [] # empty list to which tweet_details obj will be added
    counter = 0 # counter to keep track of each iteration
    # for tweet in tweepy.Cursor(api.search, q=search_term, count=100, lang='en', result_type='popular').items(): 
    for tweet in tweepy.Cursor(api.search, q=search_term, count=100, lang='en', tweet_mode='extended').items(): 
        #okay I cannot search for popularity, fine
        tweet_details = {}
        tweet_details['text'] = tweet.full_text
        data.append(tweet_details)
        
        counter += 1
        if counter == 6000: 
            break
        else:
            pass
    return data


"""
get emotion tagged twitter
search_term='COVID OR COVID-19 OR coronavirus OR Coronavirus -filter:retweets'
"""



# enjoy1000=stream_tweets('excited OR relief OR joy OR proud -filter:retweets')
# fear1000=stream_tweets('panic OR desperate OR dread OR anxiety -filter:retweets')
# anger1000=stream_tweets('fury OR frustrated OR annoyed OR bitterness -filter:retweets')
# sad1000=stream_tweets('sorrow OR grief OR misery OR discouraged -filter:retweets')
# disgust1000=stream_tweets('dislike OR loathing OR repugnant OR averse -filter:retweets')

sad6000=stream_tweets('depressed OR depression OR upset OR heartbroken OR hopeless OR sorry OR unhappy OR sad OR bereaved OR despair -filter:retweets')
anger7000=stream_tweets('angry OR disgust OR hostile OR upset OR pissed OR grouchy OR hate OR cringe OR disapprove OR enmity -filter:retweets')


import pandas as pd

# enjoy=pd.DataFrame(enjoy1000)
# enjoy= enjoy.assign(emotion='enjoyment')

# fear=pd.DataFrame(fear1000)
# fear= fear.assign(emotion='fear')

# anger=pd.DataFrame(anger1000)
# anger= anger.assign(emotion='anger')

# sad=pd.DataFrame(sad1000)
# sad= sad.assign(emotion='sadness')

sad=pd.DataFrame(sad6000)
sad= sad.assign(emotion='sadness')

anger=pd.DataFrame(anger7000)
anger= anger.assign(emotion='anger')

# disgust=pd.DataFrame(disgust1000)
# disgust= disgust.assign(emotion='disgust')

combined=[anger, sad]

combd=pd.concat(combined)

import re

def remove_url(txt):
    return " ".join(re.sub('https?://[A-Za-z0-9./]+', "", txt).split())

def remove_mention(txt):
    return " ".join(re.sub(r'@[A-Za-z0-9]+', "", txt).split())

def clean_text(df):
    df['text']=[remove_url(text) for text in df['text']] 
    df['text']=[remove_mention(text) for text in df['text']] 
    return df

cleancombd=clean_text(combd)


cleancombd.to_csv (r'D:/capstone-project/anger_sad_patch.csv', index = False, header=True)



