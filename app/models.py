from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


# define your models classes hereafter

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True
    # define here __repr__ and json methods or any common method
    # that you need for all your models

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
        column: value
        for column, value in self._to_dict().items()})

class Articles(BaseModel, db.Model):
    """Model for the articles table"""
    __tablename__ = 'articles'

    article_id = db.Column(db.String(), primary_key=True)
    headline_main = db.Column(db.String())
    author = db.Column(db.String())
    author_id = db.Column(db.String())
    pub_date = db.Column(db.String())
    section_name = db.Column(db.String())
    source = db.Column(db.String())
    type_of_material = db.Column(db.String())
    web_url = db.Column(db.String())
    word_count = db.Column(db.String())
    text = db.Column(db.String())
    byline_person_0_firstname = db.Column(db.String())
    keywords_1_value = db.Column(db.String())
    snippet = db.Column(db.String())
    byline_person_0_lastname = db.Column(db.String())
    junk = db.Column(db.String())
    keywords_2_value= db.Column(db.String())
    byline_person_0_middlename= db.Column(db.String())
    keywords_0_value= db.Column(db.String())

    