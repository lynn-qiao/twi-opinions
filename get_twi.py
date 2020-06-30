# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 22:47:51 2020

@author: xqiao
"""

#goal 1: get twitter data / hydrate it








#goal 2: filter out non-us twitter, label with state abbr
#the output should be a dataframe with 2 column 'place' and 'text'


import pandas

us_state=["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

#testfile
testfile=pandas.read_csv('testfile.csv')

def filter_non_us(testfile):
    
    df=testfile[['text','place']]
    #fill na with na-marker
    df=df.fillna(value='ZZZ')
    filtered=df[df['place'].str.contains('|'.join(us_state))]
    
    return filtered

