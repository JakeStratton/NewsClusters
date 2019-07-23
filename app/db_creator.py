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
    junk = db.Column(db.String)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    middlename = db.Column(db.String)

    def __init__(self, author):
        """"""
        self.author = author

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
    keywords_2_value= Column(String())
    byline_person_0_middlename= Column(String())
    keywords_0_value= Column(String())
    
    author = Column(String())
    author_id = Column(String())

    #add this back after populating authors table
    '''
    author_id = Column(String, ForeignKey("authors.author_id"))
    author = relationship("Author", backref=backref(
        "articles", order_by=article_id)) #this might need to be changed to author_id
    '''

    def __init__(self, headline_main, pub_date, source, type_of_material, web_url):
        """"""
        self.headline_main = headline_main
        self.pub_date = pub_date
        self.source = source
        self.type_of_material = type_of_material
        self.web_url = web_url


# create tables
Base.metadata.create_all(engine)