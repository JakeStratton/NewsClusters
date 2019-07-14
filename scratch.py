import requests
from bs4 import BeautifulSoup
import pandas as pd 
import re
import ast
import time 
from datetime import datetime
import json
from pandas.io.json import json_normalize
from flatten_json import flatten

#get month's archive from nytimes api, and save as json file
request = requests.get('https://api.nytimes.com/svc/archive/v1/2019/1.json?api-key=X4hi44ftAA1fmfGpOI6rJhLAGHSG4zOm')
data = request.json()
with open('data.json', 'w') as f:
    json.dump(data, f)

#get data from json file to dictionary
with open('data.json') as json_file:      
    data = json_file.readlines()
    # this line below may take a while. It converts all strings in list to actual json objects. 
    data = list(map(json.loads, data)) 

#create staging dataframe for next step
df = pd.DataFrame(data)

# create empty dataframe for all month's articles
articles_all_df = pd.DataFrame()  

for i in range(len(df['response'][0]['docs'])): # -1 here?  try if it doesnt work.  for loop through staging 
    try:
        article_dic = (df['response'][0]['docs'][i])
        article_dic_flat = flatten(article_dic)

        #next four lines of code are to remove keys that are making df creation error out
        article_dic_flat.pop('blog', None)
        article_dic_flat.pop('multimedia_2_legacy', None)
        article_dic_flat.pop('multimedia_3_legacy', None)
        article_dic_flat.pop('multimedia_4_legacy', None)

        print(i)

        #create dataframe from flattened and cleaned article dictionary
        article_df = pd.DataFrame(article_dic_flat, index=[0])
        
        #append article df to all articles df 
        articles_all_df = articles_all_df.append(article_df, ignore_index=True)
    
    except:
        None

