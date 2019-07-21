import psycopg2 as pg2
import sys


#connect to database
con = None
con = pg2.connect("host='localhost' dbname='newsclusters' user='jake' password='passwordjake'")   
cur = con.cursor()

#add articles table
query = '''
        CREATE TABLE articles (junk varchar(10),
            byline_person_0_firstname varchar(50),
            byline_person_0_lastname varchar(50),
            byline_person_0_middlename varchar(50),
            headline_main varchar(500),
            keywords_0_value varchar(1000),
            keywords_1_value varchar(1000),
            keywords_2_value varchar(1000),
            pub_date varchar(50),
            section_name varchar(100),
            snippet varchar(500),
            source varchar(100),
            type_of_material varchar(100),
            web_url varchar(500),
            word_count varchar(10),
            author varchar(100),
            author_id varchar(100),
            article_id varchar(500),
            text varchar(1000)
        );
        '''

cur.execute(query)
con.commit()

#import data from csv
query = '''
        COPY articles(junk,byline_person_0_firstname,byline_person_0_lastname,
        byline_person_0_middlename,headline_main,keywords_0_value,
        keywords_1_value,keywords_2_value,pub_date,section_name,snippet,
        source,type_of_material,web_url,word_count,author,author_id,
        article_id,text)
        FROM '/home/jake/data_science/NewsClusters/data/articles_2014-2018_clean.csv' 
        DELIMITER ',' 
        CSV HEADER;
        '''

cur.execute(query)
con.commit()

con.close()
