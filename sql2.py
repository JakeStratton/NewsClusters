import psycopg2 as pg2
import sys


#connect to database
con = None
con = pg2.connect("host='localhost' dbname='newsclusters' user='jake' password='passwordjake'")   
cur = con.cursor()

#add authors table
query = '''
        CREATE TABLE authors (junk varchar(10),
            firstname varchar(50),
            lastname varchar(50),
            middlename varchar(50),
            author varchar(100),
            author_id varchar(100)
        );
        '''

cur.execute(query)
con.commit()

con.close()