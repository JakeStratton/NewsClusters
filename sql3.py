import psycopg2 as pg2
import sys


#connect to database
con = None
con = pg2.connect("host='localhost' dbname='newsclusters' user='jake' password='passwordjake'")   
cur = con.cursor()

#ADD authors table
query = '''	
DROP TABLE authors;
            ;
        '''

cur.execute(query)
con.commit()

con.close()

