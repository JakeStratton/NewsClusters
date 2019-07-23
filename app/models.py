from app import db


class Author(db.Model):
    __tablename__ = "authors"

    author_id = db.Column(db.String, primary_key=True)
    author = db.Column(db.String)
    junk = db.Column(db.String)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    middlename = db.Column(db.String)

    def __init__(self, author):
        """"""
        self.author = author

    def __repr__(self):
        return "<Author: {}>".format(self.author)


class Article(db.Model):
    """"""
    __tablename__ = "articles"

    article_id = db.Column(db.String, primary_key=True)
    headline_main = db.Column(db.String)
    pub_date = db.Column(db.Date)
    source = db.Column(db.String)
    type_of_material = db.Column(db.String)
    byline_person_0_lastname = db.Column(db.String)
    web_url = db.Column(db.String)

    author = db.Column(db.String)
    author_id = db.Column(db.String)

    #add this back after populating authors table
    '''   
    author_id = db.Column(db.String, db.ForeignKey("authors.author_id"))
    author = db.relationship("Author", backref=db.backref(
        "articles", order_by=article_id), lazy=True)  #this might need to be changed to author_id
    '''

    def __init__(self, headline_main, pub_date, source, type_of_material, web_url):
        """"""
        self.headline_main = headline_main
        self.pub_date = pub_date
        self.source = source
        self.type_of_material = type_of_material
        self.web_url = web_url
