import psycopg2 as pg2
import sys


#connect to database
con = None
con = pg2.connect("host='localhost' dbname='newsclusters' user='jake' password='passwordjake'")   
cur = con.cursor()

#add authors table
query = '''
        ALTER TABLE authors
            ADD COLUMN topic_0 VARCHAR(50),
            ADD COLUMN topic_1 VARCHAR(50)
            ;
        '''

cur.execute(query)
con.commit()

con.close()

