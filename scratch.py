#gensim
import gensim 
from gensim.utils import simple_preprocess 
from gensim.parsing.preprocessing import STOPWORDS
from gensim.utils import simple_preprocess
import gensim.corpora as corpora
from gensim.models import CoherenceModel

# Plotting tools
import pyLDAvis
import pyLDAvis.gensim  
import matplotlib.pyplot as plt

#nltk
import nltk
from nltk.stem import WordNetLemmatizer, SnowballStemmer 
from nltk.stem.porter import * 
nltk.download('wordnet') 

#other
import numpy as np 
import pandas as pd
import re
from pprint import pprint


#load data
df = pd.read_csv('data/articles_2014-2018_clean.csv')

#turn text column back in to list (pandas load is making it a string)
df['text'] = df['text'].str.replace('[','').str.replace(']', '')
df['text'] = df['text'].map(lambda x: [x])

'''
def main():
    processed_docs = process_text(df['text'])
    dictionary = gensim.corpora.Dictionary(processed_docs)
    bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
    lda_model = make_lda_model()

    return None
'''

## Data Preprocessing
# Tokenize and lemmatize and stem functions
def lemmatize_stemming(text): 
    stemmer = SnowballStemmer("english")
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v')) 

def preprocess(text):
    more_stop_words = ['says', 'york', 'year', 'time', 'said', 'say']
    result=[] 
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and token not in more_stop_words and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result 


# process text
def process_text(column):
    processed_docs = []
    for i in range(len(column)):
        for doc in column[i]:
            processed_docs.append(preprocess(doc))

    return processed_docs


# process the documents
processed_docs = process_text(df['text'])

##Bag of words on the dataset

#Create a dictionary from 'processed_docs' containing the number of times a word appears 
#in the training set using gensim.corpora
#filter out extreme words
dictionary = gensim.corpora.Dictionary(processed_docs)
dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n= 100000)

#Create the Bag-of-words model for each document i.e for each document
bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]


#Use this function to show the words in the corpus and how many times they occur in a given document
def show_words(doc_num):
  bow_doc = bow_corpus[doc_num]
  for i in range(len(bow_doc)):
      print("Word {} (\"{}\") appears {} time.".format(bow_doc[i][0], 
                                                dictionary[bow_doc[i][0]], 
  bow_doc[i][1]))


# Build LDA model
def make_lda_model():
  lda_model = gensim.models.ldamodel.LdaModel(corpus=bow_corpus,
                                            id2word=dictionary,
                                            num_topics=20, 
                                            random_state=100,
                                            update_every=1,
                                            chunksize=100,
                                            passes=10,
                                            alpha='auto',
                                            per_word_topics=True)

  return lda_model


# Print the Keyword in the 10 topics
def print_topics(lda_model):
  pprint(lda_model.print_topics())
  doc_lda = lda_model[bow_corpus]

  return None


# Compute Perplexity
print('\nPerplexity: ', lda_model.log_perplexity(corpus))  # a measure of how good the model is. lower the better.

# Compute Coherence Score
coherence_model_lda = CoherenceModel(model=lda_model, texts=data_lemmatized, dictionary=dictionary, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
print('\nCoherence Score: ', coherence_lda)









'''
if __name__== "__main__":
  main()
'''

