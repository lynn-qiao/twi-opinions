
#calculate polarity of sentence

#unfortunately, sentimentr doesn't have a working python version
#try textbolb
#note that textblob is installed under python3.8.3,
# should update it into conda 
#textblob only has polarity????
#okey textblob need machine learning to categorize emotion
#the old code use lexicon approach to categorize emotion

from textblob import TextBlob
import get_twi

import pandas

#testfile
testfile=pandas.read_csv('testfile.csv')

filtered=get_twi.filter_non_us(testfile)