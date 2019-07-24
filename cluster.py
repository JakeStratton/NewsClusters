import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
import mpld3
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib

#load data
df = pd.read_csv('data/articles_2014-2018_clean.csv')

#turn text column back in to list (pandas load is making it a string)
df['text'] = df['text'].str.replace('[','').str.replace(']', '').str.replace("'", "")
#df['text'] = df['text'].map(lambda x: [x])

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
    allwords_stemmed = tokenize_and_stem(i) #for each item in 'text', tokenize/stem
    totalvocab_stemmed.extend(allwords_stemmed) #extend the 'totalvocab_stemmed' list
    
    allwords_tokenized = tokenize_only(i)
    totalvocab_tokenized.extend(allwords_tokenized)


#create a pandas DataFrame with the stemmed vocabulary
vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
print('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')



#define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(max_df=0.99, max_features=100000,
                                 min_df=0.007, stop_words='english',
                                 use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))

tfidf_matrix = tfidf_vectorizer.fit_transform(text) #fit the vectorizer to synopses

#get terms in dictionary
terms = tfidf_vectorizer.get_feature_names()

''' #this is not working
dist = 1 - cosine_similarity(tfidf_matrix)
'''


#k means clustering
num_clusters = 10
km = KMeans(n_clusters=num_clusters)
km.fit(tfidf_matrix)
clusters = km.labels_.tolist()

#save as pickle
joblib.dump(km,  'doc_cluster.pkl')

#reload the model/reassign the labels as the clusters.
km = joblib.load('doc_cluster.pkl')
clusters = km.labels_.tolist()

#create a dictionary of headlines, the text, the cluster assignment, and the author
clustered_articles = { 'article_id': df['article_id'].tolist(), 'author_id': df['author_id'].tolist(), 'headline': df['headline_main'].tolist(), 'author': df['author'].tolist(), 'text': df['text'].tolist(), 'cluster': clusters}

#create dataframe with clusters
df_clusters = pd.DataFrame(clustered_articles, index = [clusters] , 
                            columns = ['article_id', 'headline', 'author_id', 
                            'author', 'cluster', 'text'])

# get counts for each cluster
frame['cluster'].value_counts()

from __future__ import print_function

print("Top words per cluster:")
print()
#sort cluster centers by proximity to centroid
order_centroids = km.cluster_centers_.argsort()[:, ::-1] 

for i in range(num_clusters):
    print("Cluster %d words:" % i, end='')
    
    for ind in order_centroids[i, :6]: #words per cluster
        print(' %s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'), end=',')
    print() #add whitespace
    print() #add whitespace
    
    print("Cluster %d headlines:" % i, end='')
    for headline in df_clusters.ix[i]['headline'][0:100].values.tolist():
        print(' %s,' % headline, end='')
    print() #add whitespace
    print() #add whitespace
    
print()
print()



#set up colors per clusters using a dict
cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e',
                5: '#1b1e87', 6: '#d15f99', 7: '#6170b9', 8: '#e1138a', 9: '#31a22e'}

#set up cluster names using a dict
cluster_names = {0: 'World, War, New', 
                 1: 'Trump, President, Donald', 
                 2: 'Dies, Mr., Ms.', 
                 3: 'York, New, City', 
                 4: 'Year, Make, Worked',
                 5: 'States, United, Year', 
                 6: 'Games, Yankees, Teams', 
                 7: 'Books, Year, Study', 
                 8: 'Times, Year, Reports',
                 9: 'Review, Film, Theater'
                 }
