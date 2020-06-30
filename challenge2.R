setwd('D:\\backup')

raw<-read.csv("coronavirus-tweet-id-2020-04-30-23.csv")

mydata<-raw

#keep only text=en
workingApr<-subset(mydata,lang=="en")
#keep only us
mypattern<-c(state.abb,"USA")
usSubsetApr <- workingApr[grep(paste(mypattern, collapse="|"), workingApr$user_location), ]

library(sentimentr)

usSubsetApr$text<-as.character(usSubsetApr$text)
mytextApr<-get_sentences(usSubsetApr$text)

emoapr<-extract_sentiment_terms(mytextApr)
library(tm)

Aprcorpus<-Corpus(VectorSource(emoapr$negative))
Aprcorpus <- tm_map(Aprcorpus, content_transformer(tolower))
toSpace <- content_transformer(function (x , pattern ) gsub(pattern, " ", x))
Aprcorpus <- tm_map(Aprcorpus, toSpace, "/")
Aprcorpus <- tm_map(Aprcorpus, toSpace, "@")
Aprcorpus <- tm_map(Aprcorpus, toSpace, "\\|")
mystopwords<-c(stopwords("en"),'trump','pandemic','white','character','c','virus','flu',lexicon::sw_fry_100)
Aprcorpus<-tm_map(Aprcorpus, removeWords, mystopwords)
Aprcorpus <- tm_map(Aprcorpus, removeNumbers)
Aprcorpus <- tm_map(Aprcorpus, removePunctuation)
Aprcorpus <- tm_map(Aprcorpus, stripWhitespace)

library(wordcloud)

dtm <- TermDocumentMatrix(Aprcorpus)
m <- as.matrix(dtm)
v <- sort(rowSums(m),decreasing=TRUE)
d <- data.frame(word = names(v),freq=v)
head(d, 10)

set.seed(1234)
wordcloud(words = d$word, freq = d$freq, min.freq = 1,
          max.words=200, random.order=FALSE, rot.per=0.35, 
          colors=brewer.pal(8, "Dark2"))

Aprcorpus<-Corpus(VectorSource(emoapr$positive))
Aprcorpus <- tm_map(Aprcorpus, content_transformer(tolower))
toSpace <- content_transformer(function (x , pattern ) gsub(pattern, " ", x))
Aprcorpus <- tm_map(Aprcorpus, toSpace, "/")
Aprcorpus <- tm_map(Aprcorpus, toSpace, "@")
Aprcorpus <- tm_map(Aprcorpus, toSpace, "\\|")
mystopwords<-c(stopwords("en"),'trump','pandemic','white','character','c','virus','flu','new','positive',lexicon::sw_fry_100)
Aprcorpus<-tm_map(Aprcorpus, removeWords, mystopwords)
Aprcorpus <- tm_map(Aprcorpus, removeNumbers)
Aprcorpus <- tm_map(Aprcorpus, removePunctuation)
Aprcorpus <- tm_map(Aprcorpus, stripWhitespace)

dtm <- TermDocumentMatrix(Aprcorpus)
m <- as.matrix(dtm)
v <- sort(rowSums(m),decreasing=TRUE)
d <- data.frame(word = names(v),freq=v)
head(d, 10)

wordcloud(words = d$word, freq = d$freq, min.freq = 1,
          max.words=200, random.order=FALSE, rot.per=0.35, 
          colors=brewer.pal(8, "Dark2"))

sentiApr<-sentiment_by(mytextApr)
usSubsetApr<-cbind(usSubsetApr, sentiApr$ave_sentiment)
emotypeapr<-emotion(mytextApr)
emotypeapr<-subset(emotypeapr,emotion_count>0)
barplot(table(emotypeapr$emotion_type))



rawJan<-read.csv("coronavirus-tweet-id-2020-01-31-23.csv")
rawFeb<-read.csv("coronavirus-tweet-id-2020-02-29-23.csv")
rawMar<-read.csv("coronavirus-tweet-id-2020-03-31-23.csv")

mydata<-rawJan

#keep only text=en
workingJan<-subset(mydata,lang=="en")
#keep only us
usSubsetJan <- workingJan[grep(paste(mypattern, collapse="|"), workingJan$user_location), ]

usSubsetJan$text<-as.character(usSubsetJan$text)
mytextJan<-get_sentences(usSubsetJan$text)
emojan<-extract_sentiment_terms(mytextJan)
Jancorpus<-Corpus(VectorSource(emojan$negative))
Jancorpus <- tm_map(Jancorpus, content_transformer(tolower))
toSpace <- content_transformer(function (x , pattern ) gsub(pattern, " ", x))
Jancorpus <- tm_map(Jancorpus, toSpace, "/")
Jancorpus <- tm_map(Jancorpus, toSpace, "@")
Jancorpus <- tm_map(Jancorpus, toSpace, "\\|")
mystopwords<-c(stopwords("en"),'trump','pandemic','white','character','c','virus','flu',lexicon::sw_fry_100)
Jancorpus<-tm_map(Jancorpus, removeWords, mystopwords)
Jancorpus <- tm_map(Jancorpus, removeNumbers)
Jancorpus <- tm_map(Jancorpus, removePunctuation)
Jancorpus <- tm_map(Jancorpus, stripWhitespace)

dtm <- TermDocumentMatrix(Jancorpus)
m <- as.matrix(dtm)
v <- sort(rowSums(m),decreasing=TRUE)
d <- data.frame(word = names(v),freq=v)
head(d, 10)

wordcloud(words = d$word, freq = d$freq, min.freq = 1,
          max.words=200, random.order=FALSE, rot.per=0.35, 
          colors=brewer.pal(8, "Dark2"))

Jancorpus<-Corpus(VectorSource(emojan$positive))
Jancorpus <- tm_map(Jancorpus, content_transformer(tolower))
toSpace <- content_transformer(function (x , pattern ) gsub(pattern, " ", x))
Jancorpus <- tm_map(Jancorpus, toSpace, "/")
Jancorpus <- tm_map(Jancorpus, toSpace, "@")
Jancorpus <- tm_map(Jancorpus, toSpace, "\\|")
mystopwords<-c(stopwords("en"),'trump','pandemic','white','character','c','virus','flu','confirmed','positive','new',lexicon::sw_fry_100)
Jancorpus<-tm_map(Jancorpus, removeWords, mystopwords)
Jancorpus <- tm_map(Jancorpus, removeNumbers)
Jancorpus <- tm_map(Jancorpus, removePunctuation)
Jancorpus <- tm_map(Jancorpus, stripWhitespace)

dtm <- TermDocumentMatrix(Jancorpus)
m <- as.matrix(dtm)
v <- sort(rowSums(m),decreasing=TRUE)
d <- data.frame(word = names(v),freq=v)
head(d, 10)

wordcloud(words = d$word, freq = d$freq, min.freq = 1,
          max.words=200, random.order=FALSE, rot.per=0.35, 
          colors=brewer.pal(8, "Dark2"))


sentiJan<-sentiment_by(mytextJan)
usSubsetJan<-cbind(usSubsetJan, sentiJan$ave_sentiment)

emotypejan<-emotion(mytextJan)
emotypejan<-subset(emotypejan,emotion_count>0)
barplot(table(emotypejan$emotion_type))




mydata<-rawFeb

#keep only text=en
workingFeb<-subset(mydata,lang=="en")
#keep only us
usSubsetFeb <- workingFeb[grep(paste(mypattern, collapse="|"), workingFeb$user_location), ]

usSubsetFeb$text<-as.character(usSubsetFeb$text)
mytextFeb<-get_sentences(usSubsetFeb$text)
emofeb<-extract_sentiment_terms(mytextFeb)
Febcorpus<-Corpus(VectorSource(emofeb$negative))
Febcorpuss <- tm_map(Febcorpus, content_transformer(tolower))
toSpace <- content_transformer(function (x , pattern ) gsub(pattern, " ", x))
Febcorpus <- tm_map(Febcorpus, toSpace, "/")
Febcorpus <- tm_map(Febcorpus, toSpace, "@")
Febcorpus <- tm_map(Febcorpus, toSpace, "\\|")
mystopwords<-c(stopwords("en"),'trump','pandemic','white','character','c','virus','flu',lexicon::sw_fry_100)
Febcorpus<-tm_map(Febcorpus, removeWords, mystopwords)
Febcorpus <- tm_map(Febcorpus, removeNumbers)
Febcorpus <- tm_map(Febcorpus, removePunctuation)
Febcorpus <- tm_map(Febcorpus, stripWhitespace)

dtm <- TermDocumentMatrix(Febcorpus)
m <- as.matrix(dtm)
v <- sort(rowSums(m),decreasing=TRUE)
d <- data.frame(word = names(v),freq=v)
head(d, 10)

wordcloud(words = d$word, freq = d$freq, min.freq = 1,
          max.words=200, random.order=FALSE, rot.per=0.35, 
          colors=brewer.pal(8, "Dark2"))
Febcorpus<-Corpus(VectorSource(emofeb$positive))
Febcorpuss <- tm_map(Febcorpus, content_transformer(tolower))
toSpace <- content_transformer(function (x , pattern ) gsub(pattern, " ", x))
Febcorpus <- tm_map(Febcorpus, toSpace, "/")
Febcorpus <- tm_map(Febcorpus, toSpace, "@")
Febcorpus <- tm_map(Febcorpus, toSpace, "\\|")
mystopwords<-c(stopwords("en"),'trump','pandemic','white','character','c','virus','flu','confirmed','positive','admit','patient','new',lexicon::sw_fry_100)
Febcorpus<-tm_map(Febcorpus, removeWords, mystopwords)
Febcorpus <- tm_map(Febcorpus, removeNumbers)
Febcorpus <- tm_map(Febcorpus, removePunctuation)
Febcorpus <- tm_map(Febcorpus, stripWhitespace)

dtm <- TermDocumentMatrix(Febcorpus)
m <- as.matrix(dtm)
v <- sort(rowSums(m),decreasing=TRUE)
d <- data.frame(word = names(v),freq=v)
head(d, 10)

wordcloud(words = d$word, freq = d$freq, min.freq = 1,
          max.words=200, random.order=FALSE, rot.per=0.35, 
          colors=brewer.pal(8, "Dark2"))

sentiFeb<-sentiment_by(mytextFeb)
usSubsetFeb<-cbind(usSubsetFeb, sentiFeb$ave_sentiment)
emotypefeb<-emotion(mytextFeb)
emotypefeb<-subset(emotypefeb,emotion_count>0)
barplot(table(emotypefeb$emotion_type))


mydata<-rawMar
workingMar<-subset(mydata,lang=="en")
#keep only us
usSubsetMar <- workingMar[grep(paste(mypattern, collapse="|"), workingMar$user_location), ]

usSubsetMar$text<-as.character(usSubsetMar$text)
mytextMar<-get_sentences(usSubsetMar$text)
emomar<-extract_sentiment_terms(mytextMar)
Marcorpus<-Corpus(VectorSource(emomar$negative))
Marcorpuss <- tm_map(Marcorpus, content_transformer(tolower))
toSpace <- content_transformer(function (x , pattern ) gsub(pattern, " ", x))
Marcorpus <- tm_map(Marcorpus, toSpace, "/")
Marcorpus <- tm_map(Marcorpus, toSpace, "@")
Marcorpus <- tm_map(Marcorpus, toSpace, "\\|")
mystopwords<-c(stopwords("en"),'trump','pandemic','white','character','c','virus','flu','task',lexicon::sw_fry_100)
Marcorpus<-tm_map(Marcorpus, removeWords, mystopwords)
Marcorpus <- tm_map(Marcorpus, removeNumbers)
Marcorpus <- tm_map(Marcorpus, removePunctuation)
Marcorpus <- tm_map(Marcorpus, stripWhitespace)

dtm <- TermDocumentMatrix(Marcorpus)
m <- as.matrix(dtm)
v <- sort(rowSums(m),decreasing=TRUE)
d <- data.frame(word = names(v),freq=v)
head(d, 10)

wordcloud(words = d$word, freq = d$freq, min.freq = 1,
          max.words=200, random.order=FALSE, rot.per=0.35, 
          colors=brewer.pal(8, "Dark2"))


Marcorpus<-Corpus(VectorSource(emomar$positive))
Marcorpuss <- tm_map(Marcorpus, content_transformer(tolower))
toSpace <- content_transformer(function (x , pattern ) gsub(pattern, " ", x))
Marcorpus <- tm_map(Marcorpus, toSpace, "/")
Marcorpus <- tm_map(Marcorpus, toSpace, "@")
Marcorpus <- tm_map(Marcorpus, toSpace, "\\|")
mystopwords<-c(stopwords("en"),'trump','pandemic','white','character','c','virus','flu','new','positive','confirmed',lexicon::sw_fry_100)
Marcorpus<-tm_map(Marcorpus, removeWords, mystopwords)
Marcorpus <- tm_map(Marcorpus, removeNumbers)
Marcorpus <- tm_map(Marcorpus, removePunctuation)
Marcorpus <- tm_map(Marcorpus, stripWhitespace)

dtm <- TermDocumentMatrix(Marcorpus)
m <- as.matrix(dtm)
v <- sort(rowSums(m),decreasing=TRUE)
d <- data.frame(word = names(v),freq=v)
head(d, 10)

wordcloud(words = d$word, freq = d$freq, min.freq = 1,
          max.words=200, random.order=FALSE, rot.per=0.35, 
          colors=brewer.pal(8, "Dark2"))


sentiMar<-sentiment_by(mytextMar)
usSubsetMar<-cbind(usSubsetMar, sentiMar$ave_sentiment)

emotypemar<-emotion(mytextMar)
emotypemar<-subset(emotypemar,emotion_count>0)
barplot(table(emotypemar$emotion_type))


colnames(usSubsetFeb)[35]<-'ave_sentiment'
colnames(usSubsetJan)[35]<-'ave_sentiment'
colnames(usSubsetMar)[35]<-'ave_sentiment'
colnames(usSubsetApr)[35]<-'ave_sentiment'
usSubsetFeb$month<-"Feb"
usSubsetJan$month<-"Jan"
usSubsetApr$month<-"Apr"
usSubsetMar$month<-"Mar"



compmonth<-rbind(usSubsetApr[,35:36],usSubsetFeb[,35:36],usSubsetJan[,35:36],usSubsetMar[,35:36])
compmonth$month<-factor(compmonth$month, levels=c("Jan", "Feb", "Mar","Apr"))

library(ggplot2)
k<-ggplot(compmonth, aes(x=ave_sentiment, fill=month, color=month ))+ 
         geom_histogram(breaks=seq(-1.5,1.5, by=.1), position="identity", alpha=.6)
k + facet_grid(. ~ month)









#try to get state?
#get rid of unclear location, only keep those who have state marked
library(dplyr)
library(stringr)
mynewpattern<-state.abb
#remove anything not capitalized
test<-sapply(str_extract_all(usSubsetApr$user_location, "\\b[A-Z]+\\b"), paste, collapse= ' ')
#remove anything more than 3 characters


#then do the match

test<-as.data.frame(test)
test1<-filter(test, str_detect(test, paste(mynewpattern, collapse="|"))== "TRUE")


