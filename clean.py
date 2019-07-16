import pandas as pd 

def main():
    df = combine()
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
    cols_to_keep = ['_id',
    'byline_person_0_firstname',
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


    ###Preprocesing

    #convert headline and leads to list of a string
    df['text'] = df['headline_main'] + '... ' + df['snippet']
    df['snippet'] = df['snippet'].map(lambda x: [x])
    df['headline_main'] = df['headline_main'].map(lambda x: [x])
    df['text'] = df['text'].map(lambda x: [x])

    return df

if __name__== "__main__":
  main()