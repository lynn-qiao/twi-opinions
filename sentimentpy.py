
#calculate polarity of sentence

#unfortunately, sentimentr doesn't have a working python version
#try textbolb
#note that textblob is installed under python3.8.3,
# should update it into conda 
#textblob only has polarity????
#okey textblob need machine learning to categorize emotion
#the old code use lexicon approach to categorize emotion


from nrclex import NRCLex

import get_twi

import pandas

#testfile
testfile=pandas.read_csv('testfile.csv')

filtered=get_twi.filter_non_us(testfile)

text_object = NRCLex('Ridiculous. He is completely blowing this and letting people die. https://t.co/5ll3Uad1Rh') #should be a filtered text
text_object.words #return words
text_object.sentences #return sentense
text_object.affect_list #return affect list, just a list of evaluated affect for each words
text_object.affect_dict #display each word with evaluation criteria
#Return raw emotional counts.
text_object.raw_emotion_scores
#Return highest emotions.
text_object.top_emotions
#Return affect frequencies.
text_object.affect_frequencies