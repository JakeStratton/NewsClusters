# NewsClusters

## Background
Recently, my girlfriend got a new job as a media strategist for an environmental organization. She'd never worked in the NY area before, so she faced the tough task of learning about the different reporters specific to the northeast region. Individuals who work in communications and public relations, often need to find reporters to write about issues that are important to their organization. But how could they find these new authors without actually reading their stories? I  had an idea - what about a machine learning application that would intake text, assign topics based on content, and allow her to search for unknown reporters based on topics they write about. She could then also see which other reporters write about similar topics, allowing her to find out about nrew reporters without actually searching through the news and reading all of their stories.

## Approach
* Data Collection
* Data Cleaning
* Topic Modeling
* Clustering
* Web Interface

## Data Collection
I decided to use the last five years of New York Times articles, but only the headline and lead of each article.  The data is offered for free by the NYTimes in json format using their Archive API.

I set up an EC2 instance using AWS, and created a python script that connected to the API, downloaded the archives one month at a time, and then pre-cleaned and combined the months in to year long dataframes.

In all, I collected more than 230,000 articles written by over 13k different authors going back through 2014.

## Data Cleaning
After gathering the data, a number of steps were taken to clean the data for topic anlysis.
* Unneeded columns were removed.
* Articles with more than one author were removed.
* Author IDs wwere created using first, middle, and last name.
* Article IDs were created using the tail of the URL.
* Text was cleaned for punctuation and case.
* Headline and lead were combined in to one column for NLP.
* Duplicate articles were removed.

After cleaning, I ended up with 197,603 articles written by 12,703 different authors.

## Topic Modeling
I decided to use LDA to perform topic modeling. I started by using gensim's LDA package, and I performed the following preprocessing tasks:
* Stopwords were removed.
* Text was stemmed and lemmitized using gensim's default settings.
* Bigrams and trigrams were created.
* Created word corpus.

I randomly chose 8, 10, 16, and 20 topics, and I didn't get very good results. My best result was a coherence score of .26 using 10 topics.  You can see from the plot below (created using pyLDAvis) that the topics are overlappig one another, and there is very little clarity in the topics - the words don't allow for any kind of logical inference.

<INSERT LINK TO LDAVIS HERE>


I then decided to try using the Mallet LDA package, created by UMASS and Gensim has a wrapper for it so that you can easily apply it on top of the Gensim preprocessing.   I also made the following tweaks to preproceesing and recreated the corpus.
* Text was stemmed and lemmitized, but only nouns and verbs were included.  Adjectives and adverbs were ignored.
* Extreme words were removed.  Words that occurred in more than 50% of documents were ignored, and words that were in less than 15 documents total were ignored.

I then created a for loop to try different numbers of topics, and recorded the coherence score for each nuber of toics, and I discovered that there was a signficant increase in coherence score until about 22 topics, at which point the score leveled off. 

![alt text](plots/coherence_10-32.png "Coherence Scores")

Using that information, I ran the modelu using the preprocessing updates, Mallet LDA, and 22 topics, and this produced extremely clear results.  The coherence score more than doubled to .57, and you can see teh clarity in the topics below.

<INSERT LINK TO LDAVIS HERE>

It was extremely easy top infer human-useable topics from the words representing each topic:

<INSERT TOPIC LIST>

## Clustering


## Web Interface


## Next Steps
The next step is to organize the data in to a SQL database that makes sense.  I am considering having a table for reporters, and a table for articles.

