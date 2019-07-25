import psycopg2 as pg2
import sys


#connect to database
con = None
con = pg2.connect("host='localhost' dbname='newsclusters' user='jake' password='passwordjake'")   
cur = con.cursor()

#add authors table
query = '''
        CREATE TABLE authors (junk varchar(10),
            byline_person_0_firstname varchar(50),
            byline_person_0_middlename varchar(50),
            byline_person_0_lastname varchar(50),
            author varchar(100),
            author_id varchar(100),
            topic_num_0 NUMERIC,
            topic_num_1 NUMERIC,
            topic_num_2 NUMERIC,
            topic_num_3 NUMERIC,
            topic_num_4 NUMERIC,
            topic_num_5 NUMERIC,
            topic_num_6 NUMERIC,
            topic_num_7 NUMERIC,
            topic_num_8 NUMERIC,
            topic_num_9 NUMERIC,
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
            topic_num_21 NUMERIC,
            total_articles NUMERIC,
            topic_num_0_perc NUMERIC,
            topic_num_1_perc NUMERIC,
            topic_num_2_perc NUMERIC,
            topic_num_3_perc NUMERIC,
            topic_num_4_perc NUMERIC,
            topic_num_5_perc NUMERIC,
            topic_num_6_perc NUMERIC,
            topic_num_7_perc NUMERIC,
            topic_num_8_perc NUMERIC,
            topic_num_9_perc NUMERIC,
            topic_num_10_perc NUMERIC,
            topic_num_11_perc NUMERIC,
            topic_num_12_perc NUMERIC,
            topic_num_13_perc NUMERIC,
            topic_num_14_perc NUMERIC,
            topic_num_15_perc NUMERIC,
            topic_num_16_perc NUMERIC,
            topic_num_17_perc NUMERIC,
            topic_num_18_perc NUMERIC,
            topic_num_19_perc NUMERIC,
            topic_num_20_perc NUMERIC,
            topic_num_21_perc NUMERIC,
            dominant_topic_num NUMERIC,
            dominant_topic_name VARCHAR(50)
            );
        '''

cur.execute(query)
con.commit()


#import data from csv
query = '''
        COPY authors(junk,author_id,
            byline_person_0_firstname,
            byline_person_0_middlename,
            byline_person_0_lastname,
            author,
            topic_num_0,
            topic_num_1,
            topic_num_2,
            topic_num_3,
            topic_num_4,
            topic_num_5,
            topic_num_6,
            topic_num_7,
            topic_num_8,
            topic_num_9,
            topic_num_10,
            topic_num_11,
            topic_num_12,
            topic_num_13,
            topic_num_14,
            topic_num_15,
            topic_num_16,
            topic_num_17,
            topic_num_18,
            topic_num_19,
            topic_num_20,
            topic_num_21,
            total_articles,
            topic_num_0_perc,
            topic_num_1_perc,
            topic_num_2_perc,
            topic_num_3_perc,
            topic_num_4_perc,
            topic_num_5_perc,
            topic_num_6_perc,
            topic_num_7_perc,
            topic_num_8_perc,
            topic_num_9_perc,
            topic_num_10_perc,
            topic_num_11_perc,
            topic_num_12_perc,
            topic_num_13_perc,
            topic_num_14_perc,
            topic_num_15_perc,
            topic_num_16_perc,
            topic_num_17_perc,
            topic_num_18_perc,
            topic_num_19_perc,
            topic_num_20_perc,
            topic_num_21_perc,
            dominant_topic_num,
            dominant_topic_name
            )
        FROM '/home/jake/data_science/NewsClusters/data/authors.csv' 
        DELIMITER ',' 
        CSV HEADER;
        '''

cur.execute(query)
con.commit()


con.close()
