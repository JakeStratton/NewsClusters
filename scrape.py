import requests
import pandas as pd 
import ast
import time 
from datetime import datetime
import json
from flatten_json import flatten


def make_many_year_dfs(num_of_years):
    '''returns a dataframe of all articles each month going back the specified number of years'''

    articles_all_years_df = make_year_df(2019)

    for i in range(1, num_of_years):
        filename = str('articles_' + str(2019 - i) + '.csv')
        articles_year_df = make_year_df(2019 - i)
        articles_year_df.to_csv(filename)
        articles_all_years_df = articles_all_years_df.append(articles_year_df, ignore_index=True)
    
    filename = str('articles_going_back_' + str(num_of_years) + '_years.csv')
    articles_all_years_df.to_csv(filename)

    return articles_all_years_df

def make_year_df(year):
    '''returns a dataframe of the year, and creates a csv.'''

    articles_year_df = pd.DataFrame()

    if year == 2019:
        # hard code month of 2019 in for now in the end of first for loop range, will change this in final tweaks
        for i in range(1,3):
            month_df = get_article_month_year(i, year)
            articles_year_df = articles_year_df.append(month_df, ignore_index=True)
        
        # save csv file from dataframe
        filename = str('articles_' + str(year) + '.csv')
        articles_year_df.to_csv(filename)
        
        return articles_year_df

    else:
        for i in range(1,13):
            month_df = get_article_month_year(i, year)
            articles_year_df = articles_year_df.append(month_df, ignore_index=True)
        
        # save csv file from dataframe
        filename = str('articles_' + str(year) + '.csv')
        articles_year_df.to_csv(filename)
        
        return articles_year_df


def get_article_month_year(month, year):
    '''returns a dataframe of all meta data of all articles published in the given month and year'''

    #set url base and end 
    url_base = 'https://api.nytimes.com/svc/archive/v1/'
    url_end = '.json?api-key=X4hi44ftAA1fmfGpOI6rJhLAGHSG4zOm'
    url = str(url_base + str(year) + '/' + str(month) + url_end)

    #get month's archive from nytimes api, and save as json file
    request = requests.get(url)
    data = request.json()
    with open('data.json', 'w') as f:
        json.dump(data, f)

    #get data from json file to dictionary
    with open('data.json') as json_file:      
        data = json_file.readlines()
        #convert all strings in list to actual json objects. 
        data = list(map(json.loads, data)) 

    #create staging dataframe for next step
    df = pd.DataFrame(data)

    # create empty dataframe for all month's articles
    articles_all_df = pd.DataFrame()  

    #loop through each article
    for i in range(len(df['response'][0]['docs'])):  # df['response'][0]['docs'] is the location to dig in to get to the article dictionary level
        try:
            article_dic = (df['response'][0]['docs'][i])
            article_dic_flat = flatten(article_dic)

            #next four lines of code are to remove keys that are making df creation error 
            article_dic_flat.pop('blog', None)
            article_dic_flat.pop('multimedia_2_legacy', None)
            article_dic_flat.pop('multimedia_3_legacy', None)
            article_dic_flat.pop('multimedia_4_legacy', None)

            print(((len(df['response'][0]['docs'])) - i), month, year)

            #create dataframe from flattened and cleaned article dictionary
            article_df = pd.DataFrame(article_dic_flat, index=[0])
            
            #append article df to all articles df 
            articles_all_df = articles_all_df.append(article_df, ignore_index=True)
        
        except:
            None

    return articles_all_df

