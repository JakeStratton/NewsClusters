import pandas as pd 

def main():
  #df = combine()
  df = clean(df)

  return df


def combine():
  df1 = pd.read_csv('data/articles_2018.csv')
  df2 = pd.read_csv('data/articles_2017.csv')
  df3 = pd.read_csv('data/articles_2016.csv')
  df4 = pd.read_csv('data/articles_2015.csv')
  df5 = pd.read_csv('data/articles_2014.csv')
  df = pd.concat([df1, df2, df3, df4, df5])
  df.to_csv('data/articles_2014-2018.csv')

  return df


def clean(df):

  ###First clean

  #remove rows based on nan (these columns must have values, otherwise remove the row)
  df = df.dropna(subset=['byline_original'])
  df = df.dropna(subset=['headline_main']) 
  df = df.dropna(subset=['byline_person_0_lastname'])
  df = df.dropna(subset=['snippet'])

  #rows to delete based on conditions
  delete_cols = df[df['type_of_material'] == 'Video'].index
  df.drop(delete_cols , inplace=True)

  delete_cols = df[df['byline_person_1_lastname'].notnull() == True].index
  df.drop(delete_cols , inplace=True)

  #remove unneeded columns
  cols_to_keep = ['byline_person_0_firstname',
  'byline_person_0_lastname',
  'byline_person_0_middlename',
  'headline_main',
  'keywords_0_value',
  'keywords_1_value',
  'keywords_2_value',
  'pub_date',
  'section_name',
  'snippet',
  'source',
  'type_of_material',
  'web_url',
  'word_count'
  ]

  df = df[cols_to_keep]
  df = df.reset_index()

  # use first, middel, and last names to create an author column
  df['byline_person_0_middlename'].fillna('None', inplace=True)
  df = df.reset_index()
  df['author'] = df[['byline_person_0_firstname', 'byline_person_0_middlename', 'byline_person_0_lastname']].apply(lambda x: ' '.join(x), axis=1)
  df['author'] = df['author'].map(lambda x: x.replace(' None ', ' ').title())

  #fill all remaining nan values - only additional keywords are missing values at this point
  df = df.fillna('None')

  #clean and lower all text columns - need to find a cleaner way to write  the following code (i should atleast make each section a one liner)
  df['byline_person_0_firstname'] = df['byline_person_0_firstname'].str.replace('[^\w\s]','')
  df['byline_person_0_firstname'] = df['byline_person_0_firstname'].str.lower()
  df['byline_person_0_firstname'] = df['byline_person_0_firstname'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

  df['byline_person_0_lastname'] = df['byline_person_0_lastname'].str.replace('[^\w\s]','')
  df['byline_person_0_lastname'] = df['byline_person_0_lastname'].str.lower()
  df['byline_person_0_lastname'] = df['byline_person_0_lastname'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

  df['byline_person_0_middlename'] = df['byline_person_0_middlename'].str.replace('[^\w\s]','')
  df['byline_person_0_middlename'] = df['byline_person_0_middlename'].str.lower()
  df['byline_person_0_middlename'] = df['byline_person_0_middlename'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

  df['headline_main'] = df['headline_main'].str.replace('[^\w\s]','')
  df['headline_main'] = df['headline_main'].str.lower()
  df['headline_main'] = df['headline_main'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

  df['keywords_0_value'] = df['keywords_0_value'].str.replace('[^\w\s]','')
  df['keywords_0_value'] = df['keywords_0_value'].str.lower()
  df['keywords_0_value'] = df['keywords_0_value'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

  df['keywords_1_value'] = df['keywords_1_value'].str.replace('[^\w\s]','')
  df['keywords_1_value'] = df['keywords_1_value'].str.lower()
  df['keywords_1_value'] = df['keywords_1_value'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

  df['keywords_2_value'] = df['keywords_2_value'].str.replace('[^\w\s]','')
  df['keywords_2_value'] = df['keywords_2_value'].str.lower()
  df['keywords_2_value'] = df['keywords_2_value'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

  df['section_name'] = df['section_name'].str.replace('[^\w\s]','')
  df['section_name'] = df['section_name'].str.lower()
  df['section_name'] = df['section_name'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

  df['snippet'] = df['snippet'].str.replace('[^\w\s]','')
  df['snippet'] = df['snippet'].str.lower()
  df['snippet'] = df['snippet'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

  df['source'] = df['source'].str.replace('[^\w\s]','')
  df['source'] = df['source'].str.lower()
  df['source'] = df['source'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

  df['type_of_material'] = df['type_of_material'].str.replace('[^\w\s]','')
  df['type_of_material'] = df['type_of_material'].str.lower()
  df['type_of_material'] = df['type_of_material'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

  #clean date column
  df['pub_date'] = df['pub_date'].str.replace('T', ' ').str.replace('0000', '').str.replace('+', '')

  #create Author ID - i need to come back and generate numerical IDs 
  df['author_id'] = df[['byline_person_0_firstname', 'byline_person_0_middlename', 'byline_person_0_lastname']].apply(lambda x: ''.join(x), axis=1)

  #create article ID - i need to come back and generate numerical IDs 
  df['article_id'] = df['web_url']
  df['article_id'] = df['article_id'].str.replace('[^\w\s]','')
  df['article_id'] = df['article_id'].str.lower()
  df['article_id'] = df['article_id'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
  df['article_id'] = df['article_id'].str.replace('httpswwwnytimescom','')

  ### NLP Preprocesing - enriching data with added columns specifically for the NLP
  #all columns will live in a postgres db, but the folowwing columns will be used for NLP

  #convert headline and leads to list of a string, after removing punctuation, lowercaseing, removing accented letters,
  # and removing duplicate rows based on text and author columns
  df['text'] = df['headline_main'] + ' ' + df['snippet']
  df['text'] = df['text'].str.replace('[^\w\s]','')
  df['text'] = df['text'].str.lower()
  df['text'] = df['text'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
  #remove duplicates
  df = df[~df.duplicated(['text', 'author'])]
  #turn text column in to a list of the string for LDA, etc.
  df['text'] = df['text'].map(lambda x: [x])

  #remove junk columns
  df = df.drop('index', axis=1)
  df = df.drop('level_0', axis=1)

  return df


if __name__== "__main__":
  main()



