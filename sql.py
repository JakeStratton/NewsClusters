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
            text varchar(1000),
            Document_No NUMERIC,
            Topic_Perc_Contrib NUMERIC,
            Keywords varchar(1000),
            topic_name varchar(100),
            topic_num NUMERIC,
            topic_num_0 NUMERIC,
            topic_num_1 NUMERIC,
            topic_num_2 NUMERIC,
            topic_num_3 NUMERIC,
            topic_num_4 NUMERIC,
            topic_num_5 NUMERIC,
            topic_num_6 NUMERIC,
            topic_num_7 NUMERIC,
            topic_num_8 NUMERIC,
            topic_num_9 NUMERIC,0
            topic_num_10 NUMERIC,
            topic_num_11 NUMERIC,
            topic_num_12 NUMERIC,
            topic_num_13 NUMERIC,
            topic_num_14 NUMERIC,
            topic_num_15 NUMERIC,
            topic_num_16 NUMERIC,
            topic_num_17 NUMERIC,
            topic_num_18 NUMERIC,
            topic_num_19 NUMERIC,
            topic_num_20 NUMERIC,
            topic_num_21 NUMERIC
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
        article_id,text,Document_No,Topic_Perc_Contrib,Keywords,topic_name,
        topic_num,topic_num_0,topic_num_1,topic_num_2,topic_num_3,topic_num_4,
        topic_num_5,topic_num_6,topic_num_7,topic_num_8,topic_num_9,topic_num_10,
        topic_num_11,topic_num_12,topic_num_13,topic_num_14,topic_num_15,
        topic_num_16,topic_num_17,topic_num_18,topic_num_19,topic_num_20,
        topic_num_21)
        FROM '/home/jake/data_science/NewsClusters/data/articles.csv' 
        DELIMITER ',' 
        CSV HEADER;
        '''

cur.execute(query)
con.commit()

con.close()
