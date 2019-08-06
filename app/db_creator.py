from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('postgresql://jake:passwordjake@localhost:5432/newsclusters', echo=True)
Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"

    author_id = Column(String, primary_key=True)
    author = Column(String)
    junk = Column(String)
    byline_person_0_firstname = Column(String)
    byline_person_0_lastname = Column(String)
    byline_person_0_middlename = Column(String)
    topic_num_0 = Column(Integer())
    topic_num_1 = Column(Integer())
    topic_num_2 = Column(Integer())
    topic_num_3 = Column(Integer())
    topic_num_4 = Column(Integer())
    topic_num_5 = Column(Integer())
    topic_num_6 = Column(Integer())
    topic_num_7 = Column(Integer())
    topic_num_8 = Column(Integer())
    topic_num_9 = Column(Integer())
    topic_num_10 = Column(Integer())
    topic_num_11 = Column(Integer())
    topic_num_12 = Column(Integer())
    topic_num_13 = Column(Integer())
    topic_num_14 = Column(Integer())
    topic_num_15 = Column(Integer())
    topic_num_16 = Column(Integer())
    topic_num_17 = Column(Integer())
    topic_num_18 = Column(Integer())
    topic_num_19 = Column(Integer())
    topic_num_20 = Column(Integer())
    topic_num_21 = Column(Integer())
    topic_num_22 = Column(Integer())
    topic_num_23 = Column(Integer())
    topic_num_24 = Column(Integer())
    topic_num_25 = Column(Integer())
    topic_num_26 = Column(Integer())
    topic_num_27 = Column(Integer())
    topic_num_28 = Column(Integer())
    topic_num_29 = Column(Integer())
    topic_num_30 = Column(Integer())
    topic_num_31 = Column(Integer())
    topic_num_32 = Column(Integer())
    topic_num_33 = Column(Integer())
    total_articles = Column(Integer())
    topic_num_0_perc = Column(Integer())
    topic_num_1_perc = Column(Integer())
    topic_num_2_perc = Column(Integer())
    topic_num_3_perc = Column(Integer())
    topic_num_4_perc = Column(Integer())
    topic_num_5_perc = Column(Integer())
    topic_num_6_perc = Column(Integer())
    topic_num_7_perc = Column(Integer())
    topic_num_8_perc = Column(Integer())
    topic_num_9_perc = Column(Integer())
    topic_num_10_perc = Column(Integer())
    topic_num_11_perc = Column(Integer())
    topic_num_12_perc = Column(Integer())
    topic_num_13_perc = Column(Integer())
    topic_num_14_perc = Column(Integer())
    topic_num_15_perc = Column(Integer())
    topic_num_16_perc = Column(Integer())
    topic_num_17_perc = Column(Integer())
    topic_num_18_perc = Column(Integer())
    topic_num_19_perc = Column(Integer())
    topic_num_20_perc = Column(Integer())
    topic_num_21_perc = Column(Integer())
    topic_num_22_perc = Column(Integer())
    topic_num_23_perc = Column(Integer())
    topic_num_24_perc = Column(Integer())
    topic_num_25_perc = Column(Integer())
    topic_num_26_perc = Column(Integer())
    topic_num_27_perc = Column(Integer())
    topic_num_28_perc = Column(Integer())
    topic_num_29_perc = Column(Integer())
    topic_num_30_perc = Column(Integer())
    topic_num_31_perc = Column(Integer())
    topic_num_32_perc = Column(Integer())
    topic_num_33_perc = Column(Integer())
    dominant_topic_num = Column(Integer())
    dominant_topic_name = Column(String())
    def __init__(self, author, author_id, dominant_topic_name, total_articles):
        """"""
        self.author = author
        self.author_id = author_id
        self.dominant_topic_name = dominant_topic_name
        self.total_articles = total_articles

    def __repr__(self):
        return "<Author: {}>".format(self.author)


class Article(Base):
    """"""
    __tablename__ = 'articles'

    article_id = Column(String(), primary_key=True)
    headline_main = Column(String())
    pub_date = Column(String())
    section_name = Column(String())
    source = Column(String())
    type_of_material = Column(String())
    web_url = Column(String())
    word_count = Column(String())
    text = Column(String())
    byline_person_0_firstname = Column(String())
    keywords_1_value = Column(String())
    snippet = Column(String())
    byline_person_0_lastname = Column(String())
    junk = Column(String())
    keywords_2_value = Column(String())
    byline_person_0_middlename = Column(String())
    keywords_0_value = Column(String())
    topic_name = Column(String())

    '''
    author = Column(String())
    author_id = Column(String())
    '''
 
    author_id = Column(String, ForeignKey("authors.author_id"))
    author = relationship("Author", backref=backref(
        "articles", order_by=article_id)) #this might need to be changed to author_id


    def __init__(self, headline_main, pub_date, source, type_of_material, web_url, topic_name):
        """"""
        self.headline_main = headline_main
        self.pub_date = pub_date
        self.source = source
        self.type_of_material = type_of_material
        self.web_url = web_url
        self.topic_name = topic_name



# create tables
Base.metadata.create_all(engine)


