import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import itertools
import scipy.stats as scs
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score, silhouette_samples
import matplotlib
from IPython.display import HTML, display


import pandas as pd
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist, squareform

#load data
df = pd.read_csv('data/authors.csv')

df = df.nlargest(100, ['total_articles']) 

#remove unneeded columns for clustering
cols_to_delete = ['Unnamed: 0',
                'byline_person_0_firstname',
                'byline_person_0_middlename',
                'byline_person_0_lastname',
                'author_id', 'dominant_topic_name', 
                'topic_num_0',
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
                'topic_num_21',
                'total_articles',
                'dominant_topic',
                'author_id']

df = df.drop(cols_to_delete, axis=1)
df = df.set_index('author')

def make_dendrogram(dataframe, linkage_method, metric, color_threshold=None):
    '''
    This function creates and plots the dendrogram created by hierarchical clustering.
    
    INPUTS: Pandas Dataframe, string, string, int
    
    OUTPUTS: None
    '''
    distxy = squareform(pdist(dataframe.values, metric=metric))
    Z = linkage(distxy, linkage_method)
    plt.figure(figsize=(20, 8))
    plt.title('Top 100 Authors based on Total Articles')
    plt.xlabel('Author')
    plt.ylabel('Distance')
    dendrogram(
        Z,
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=8.,  # font size for the x axis labels
        labels = dataframe.index,
        color_threshold = color_threshold
    )
    plt.tight_layout()
    plt.show()


linktype = 'average'
metric = 'euclid'
make_dendrogram(df, linktype, metric, color_threshold=None)