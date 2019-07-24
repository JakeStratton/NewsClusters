import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
import mpld3


#load data
df = pd.read_csv('data/articles_2014-2018_clean.csv')

#turn text column back in to list (pandas load is making it a string)
df['text'] = df['text'].str.replace('[','').str.replace(']', '')
df['text'] = df['text'].map(lambda x: [x])

#create two lists, one for article_id and one for text
text = df['text'].tolist()

# load nltk's English stopwords as variable called 'stopwords'
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(['say', 'says', 'said', 'abov', 'afterward', 'alon', 
                'alreadi', 'alway', 'ani', 'anoth', 'anyon', 'anyth', 
                'anywher', 'becam', 'becaus', 'becom', 'befor', 'besid', 
                'cri', 'describ', 'dure', 'els', 'elsewher', 'empti', 
                'everi', 'everyon', 'everyth', 'everywher', 'fifti', 
                'forti', 'henc', 'hereaft', 'herebi', 'howev', 'hundr', 
                'inde', 'mani', 'meanwhil', 'moreov', 'nobodi', 'noon', 
                'noth', 'nowher', 'onc', 'onli', 'otherwis', 'ourselv', 
                'perhap', 'pleas', 'sever', 'sinc', 'sincer', 'sixti', 
                'someon', 'someth', 'sometim', 'somewher', 'themselv', 
                'thenc', 'thereaft', 'therebi', 'therefor', 'togeth', 
                'twelv', 'twenti', 'veri', 'whatev', 'whenc', 'whenev', 
                'wherea', 'whereaft', 'wherebi', 'wherev', 'whi', 'yourselv'])


# load nltk's SnowballStemmer as variabled 'stemmer'
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")


# define a tokenizer and stemmer which returns the set of stems in the text that it is passed
def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

 
def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


#use extend so it's a big flat list of vocab
totalvocab_stemmed = []
totalvocab_tokenized = []
for i in text:
    allwords_stemmed = tokenize_and_stem(i) #for each item in 'synopses', tokenize/stem
    totalvocab_stemmed.extend(allwords_stemmed) #extend the 'totalvocab_stemmed' list
    
    allwords_tokenized = tokenize_only(i)
    totalvocab_tokenized.extend(allwords_tokenized)


#create a pandas DataFrame with the stemmed vocabulary
vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
print('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')



from sklearn.feature_extraction.text import TfidfVectorizer

#define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(max_df=0.99, max_features=100000,
                                 min_df=0.007, stop_words='english',
                                 use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))

tfidf_matrix = tfidf_vectorizer.fit_transform(text) #fit the vectorizer to synopses

print(tfidf_matrix.shape)
