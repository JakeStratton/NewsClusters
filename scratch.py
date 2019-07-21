import gensim 
from gensim.utils import simple_preprocess 
from gensim.parsing.preprocessing import STOPWORDS 
from nltk.stem import WordNetLemmatizer, SnowballStemmer 
from nltk.stem.porter import * 
import numpy as np 
import nltk
# nltk.download('wordnet')


def main():
    #processed_docs = process_text(df['text'])
    #dictionary = gensim.corpora.Dictionary(processed_docs)
    #bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
    return None


## Data Preprocessing

# Tokenize and lemmatize and stem functions

def lemmatize_stemming(text): 
    stemmer = SnowballStemmer("english")
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v')) 

def preprocess(text):
    result=[] 
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result 



# process text

def process_text(column):
    processed_docs = []
    for i in range(len(column)):
        for doc in column[i]:
            processed_docs.append(preprocess(doc))
    
    dictionary = gensim.corpora.Dictionary(processed_docs)
    
    return processed_docs


##Bag of words on the dataset

#Create a dictionary from 'processed_docs' containing the number of times a word appears 
#in the training set using gensim.corpora.Dictionary and call it 'dictionary'

dictionary = gensim.corpora.Dictionary(processed_docs)
bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

'''
OPTIONAL STEP
Remove very rare and very common words -
the below would filter:
- words appearing less than 15 times
- words appearing in more than 10% of all documents

dictionary.filter_extremes(no_below=15, no_above=0.1, keep_n= 100000)
'''

#Create the Bag-of-words model for each document i.e for each document we create a dictionary reporting how many
#words and how many times those words appear. Save this to 'bow_corpus'

#bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]





if __name__== "__main__":
  main()



  scp -i NewsClusters.pem ec2-user@ec2-52-202-226-218.compute-1.amazonaws.com:/home/ec2-user/NewsClusters/articles_2018.csv ~/data_science/NewsClusters/data/articles_2018.csv


