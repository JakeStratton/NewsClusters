import re
import numpy as np
import pandas as pd
from pprint import pprint

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# spacy for lemmatization
import spacy

# Plotting tools
import pyLDAvis
import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt

# Enable logging for gensim - optional
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

# NLTK Stop words
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(['say', 'says', 'said', 'year', 'time', 'way',
                        'week', 'make', 'thursday', 'monday', 'tuesday', 'wednesday', 'friday'  ])

#show all padas columns for readability
pd.set_option('display.max_columns', None)

#import data
df = pd.read_csv('data/articles_2014-2018_clean.csv')
df = df[['text', 'article_id', 'author_id']]
df.head()

#turn text column back in to list (pandas load is making it a string)
df['text'] = df['text'].str.replace('[','').str.replace(']', '').str.replace("'", "")
#df['text'] = df['text'].map(lambda x: [x])

# Convert to list
data = df['text'].values.tolist()

#tokenize
def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations

data_words = list(sent_to_words(data))

# Build the bigram and trigram models
bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
trigram = gensim.models.Phrases(bigram[data_words], threshold=100)  

# Faster way to get a sentence clubbed as a trigram/bigram
bigram_mod = gensim.models.phrases.Phraser(bigram)
trigram_mod = gensim.models.phrases.Phraser(trigram)

# See trigram example
print(trigram_mod[bigram_mod[data_words[0]]])

# Define functions for stopwords, bigrams, trigrams and lemmatization
def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'VERB']):  #, 'ADJ', 'VERB', 'ADV'
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

# Remove Stop Words
data_words_nostops = remove_stopwords(data_words)

# Form Bigrams
data_words_bigrams = make_bigrams(data_words_nostops)

# Initialize spacy 'en' model, keeping only tagger component (for efficiency)
# python3 -m spacy download en
nlp = spacy.load('en', disable=['parser', 'ner'])

# Do lemmatization keeping only noun, vb
data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'VERB' ]) #'ADV', 'ADJ'

# Create Dictionary and remove extremely common and rare words
id2word = corpora.Dictionary(data_lemmatized)
id2word.filter_extremes(no_below=15, no_above=0.5, keep_n= 100000)

# Create Corpus
texts = data_lemmatized

# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in texts]

# Human readable format of corpus (term-frequency)
[[(id2word[id], freq) for id, freq in cp] for cp in corpus[:1]]

# Build LDA model #1
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=22, 
                                           random_state=1,
                                           update_every=1,
                                           chunksize=500,
                                           passes=10,
                                           alpha='auto')

'''
# Build LDA model #2
lda_model2 = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=16, 
                                           random_state=1,
                                           update_every=1,
                                           chunksize=500,
                                           passes=10,
                                           alpha='auto')
'''

# Print the Keyword in the 10 topics
pprint(lda_model.print_topics())
doc_lda = lda_model[corpus]

# Compute Perplexity
print('\nPerplexity: ', lda_model.log_perplexity(corpus))  # a measure of how good the model is. lower the better.

# Compute Coherence Score
coherence_model_lda = CoherenceModel(model=lda_model, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
print('\nCoherence Score: ', coherence_lda) 


# Visualize the topics
pyLDAvis.disable_notebook()
vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
#save as HTML
pyLDAvis.save_html(vis, 'lda.html')

# try using mallets LDA - gensim has a wrapper to allow it to be buuilt on top of the gensim lda
mallet_path = '/home/jake/data_science/mallet/mallet-2.0.8/bin/mallet' 
ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=22, id2word=id2word)

# Show Topics from mallet
pprint(ldamallet.show_topics(formatted=False))

# Compute Coherence Score from mallet
coherence_model_ldamallet = CoherenceModel(model=ldamallet, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
coherence_ldamallet = coherence_model_ldamallet.get_coherence()
print('\nCoherence Score: ', coherence_ldamallet)


#use this to determine how many topics to use.  it loops through and tries the model many different times
def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=3):
    """
    Compute c_v coherence for various number of topics

    Parameters:
    ----------
    dictionary : Gensim dictionary
    corpus : Gensim corpus
    texts : List of input texts
    limit : Max num of topics

    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=num_topics, id2word=id2word)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values

#run the above compute coherence values to find the best
# Can take a long time to run.
model_list, coherence_values = compute_coherence_values(dictionary=id2word, 
                                                        corpus=corpus, texts=data_lemmatized, 
                                                        start=10, limit=41, step=2)

#plot results of the multiple mallet topic tries
# Show graph
limit=41; start=10; step=2;
x = range(start, limit, step)
plt.plot(x, coherence_values)
plt.title('Coherence Score per Number of Topics')
plt.xlabel("Num Topics")
plt.ylabel("Coherence score")
plt.legend(("coherence_values"), loc='best')
plt.show()

# Print the coherence scores
for m, cv in zip(x, coherence_values):
    print("Num Topics =", m, " has Coherence Value of", round(cv, 4))

# Select the model and print the topics
optimal_model = model_list[6] #model 6 is the best (22 topics)
model_topics = optimal_model.show_topics(formatted=False)
pprint(optimal_model.print_topics(num_words=20))

#create a table to showwhich topic applies to each document
def format_topics_sentences(ldamodel=lda_model, corpus=corpus, texts=data):
    # Init output
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row in enumerate(ldamodel[corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return(sent_topics_df)


df_topic_sents_keywords = format_topics_sentences(ldamodel=optimal_model, corpus=corpus, texts=data)

# create df of each article with associated dominant topic
df_dominant_topic = df_topic_sents_keywords.reset_index()
df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']


#add topics to articles df and clean up unneded columns.
df_articles = pd.read_csv('data/articles_2014-2018_clean.csv')
df_articles = pd.concat([df_articles, df_dominant_topic], axis=1, sort=False)
df_articles = df_articles.drop(['Text', 'Unnamed: 0'], axis=1)


#create topics df
# Number of Documents for Each Topic
topic_counts = df_topic_sents_keywords['Dominant_Topic'].value_counts().sort_index() 
# Percentage of Documents for Each Topic
topic_contribution = round(topic_counts/topic_counts.sum(), 4).sort_index() 
# Topic Number and Keywords
topic_num_keywords = df_topic_sents_keywords[['Dominant_Topic', 'Topic_Keywords']]
topic_num_keywords = topic_num_keywords.drop_duplicates(subset ="Dominant_Topic").set_index('Dominant_Topic')
topic_num_keywords = topic_num_keywords.sort_index()
# Concatenate 
df_topics = pd.concat([topic_num_keywords, topic_counts, topic_contribution], axis=1, sort=False)
# Change Column names and re-index to get topic num as a column
df_topics.columns = ['topic_keywords', 'num_docs', 'percent_docs']
df_topics.reset_index(level=0, inplace=True) 
df_topics.columns = ['topic', 'topic_keywords', 'num_docs', 'percent_docs']

#create topic names (manually inferred)
topic_names = ['NY Local', 'Politics and Elections', 'Foreign Affairs',
                'Health and Science', 'War and Conflict', 'News about News', 
                'Travel', 'Technology', 'Fashion', 'Local Sports', 'National Sports',
                'Education', 'Music', 'Economy', 'Government', 'Law', 'Labor', 
                'Crime', 'World News', 'Film', 'Theater', 'Social']

#add topic names to articles df and save
mydict = {v: k for v, k in enumerate(topic_names)} 
df_articles['topic_name'] = df_articles['Dominant_Topic'].map(mydict) 


#insert topic names in to topics df
topic_names = pd.Series(topic_names)
df_topics = pd.concat([df_topics, topic_names], axis=1, sort=False)
df_topics.columns = ['topic', 'topic_keywords', 'num_docs', 'percent_docs', 'topic_name']
#save topics df
df_topics.to_csv('data/topics.csv')

#OHE the dominant topic column
df_articles['Dominant_Topic'] = df_articles['Dominant_Topic'].astype('int16')
df_articles['topic_num'] = df_articles['Dominant_Topic']
df_articles = pd.get_dummies(df_articles, prefix=['topic_num'], columns=['Dominant_Topic'])  
#save df_articles
df_articles.to_csv('data/articles.csv')

#convert mallet model to gensim in order to display using pyLDAvis
lda_model_mallet = gensim.models.wrappers.ldamallet.malletmodel2ldamodel(ldamallet)

# Visualize the mallet LDA topics
pyLDAvis.disable_notebook()
mallet_vis = pyLDAvis.gensim.prepare(lda_model_mallet, corpus, id2word)
#save as HTML
pyLDAvis.save_html(mallet_vis, 'lda_mallet.html')

#create authors df with counts of articles in each topic
df_authors = df_articles[['author_id', 'byline_person_0_firstname', 'byline_person_0_middlename', 'byline_person_0_lastname', 'author']]
df_authors = df_authors.drop_duplicates().set_index('author_id')
df_authors.reset_index(level=0, inplace=True)
df_authors_sums = df_articles.groupby(['author_id']).sum()
df_authors_sums = df_authors_sums.drop(['Unnamed: 0',  'Document_No',  'Topic_Perc_Contrib',  'topic_num'], axis=1) 
df_authors_sums.reset_index(level=0, inplace=True)
df_authors = df_authors.set_index('author_id').join(df_authors_sums.set_index('author_id'))
df_authors = df_authors.dropna(axis='rows')

#add percentage columns to authors df #find a more pythonic way to do this!!!!!
df_authors['total_articles'] = df_authors.sum(axis=1)  #total articles for each author
df_authors['topic_num_0_perc'] = df_authors['topic_num_0'] / df_authors['total_articles'] 
df_authors['topic_num_1_perc'] = df_authors['topic_num_1'] / df_authors['total_articles'] 
df_authors['topic_num_2_perc'] = df_authors['topic_num_2'] / df_authors['total_articles'] 
df_authors['topic_num_3_perc'] = df_authors['topic_num_3'] / df_authors['total_articles'] 
df_authors['topic_num_4_perc'] = df_authors['topic_num_4'] / df_authors['total_articles'] 
df_authors['topic_num_5_perc'] = df_authors['topic_num_5'] / df_authors['total_articles'] 
df_authors['topic_num_6_perc'] = df_authors['topic_num_6'] / df_authors['total_articles'] 
df_authors['topic_num_7_perc'] = df_authors['topic_num_7'] / df_authors['total_articles'] 
df_authors['topic_num_8_perc'] = df_authors['topic_num_8'] / df_authors['total_articles'] 
df_authors['topic_num_9_perc'] = df_authors['topic_num_9'] / df_authors['total_articles'] 
df_authors['topic_num_10_perc'] = df_authors['topic_num_10'] / df_authors['total_articles'] 
df_authors['topic_num_11_perc'] = df_authors['topic_num_11'] / df_authors['total_articles'] 
df_authors['topic_num_12_perc'] = df_authors['topic_num_12'] / df_authors['total_articles'] 
df_authors['topic_num_13_perc'] = df_authors['topic_num_13'] / df_authors['total_articles'] 
df_authors['topic_num_14_perc'] = df_authors['topic_num_14'] / df_authors['total_articles'] 
df_authors['topic_num_15_perc'] = df_authors['topic_num_15'] / df_authors['total_articles'] 
df_authors['topic_num_16_perc'] = df_authors['topic_num_16'] / df_authors['total_articles'] 
df_authors['topic_num_17_perc'] = df_authors['topic_num_17'] / df_authors['total_articles'] 
df_authors['topic_num_18_perc'] = df_authors['topic_num_18'] / df_authors['total_articles'] 
df_authors['topic_num_19_perc'] = df_authors['topic_num_19'] / df_authors['total_articles'] 
df_authors['topic_num_20_perc'] = df_authors['topic_num_20'] / df_authors['total_articles'] 
df_authors['topic_num_21_perc'] = df_authors['topic_num_21'] / df_authors['total_articles'] 
df_authors = df_authors.round(2) #round off for easy percentage reading

#add dominant topic for each author
df_authors['dominant_topic'] = df_authors[['topic_num_0',
                                        'topic_num_1',
                                        'topic_num_2',
                                        'topic_num_3',
                                        'topic_num_4',
                                        'topic_num_5',
                                        'topic_num_6',
                                        'topic_num_7',
                                        'topic_num_8',
                                        'topic_num_9',
                                        'topic_num_10',
                                        'topic_num_11',
                                        'topic_num_12',
                                        'topic_num_13',
                                        'topic_num_14',
                                        'topic_num_15',
                                        'topic_num_16',
                                        'topic_num_17',
                                        'topic_num_18',
                                        'topic_num_19',
                                        'topic_num_20',
                                        'topic_num_21'
                                        ]].idxmax(axis=1)

df_authors['dominant_topic'] = df_authors['dominant_topic'].str.replace('topic_num_', '')
df_authors['dominant_topic'] = df_authors['dominant_topic'].astype('int16')

#add topic names to authors df and save
mydict = {v: k for v, k in enumerate(topic_names)} 
df_authors['dominant_topic_name'] = df_authors['dominant_topic'].map(mydict) 
df_authors = df_authors.reset_index()
df_authors.to_csv('data/authors.csv')