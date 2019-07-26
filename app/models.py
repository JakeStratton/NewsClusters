from app import db


class Author(db.Model):
    __tablename__ = "authors"

    author_id = db.Column(db.String, primary_key=True)
    author = db.Column(db.String)
    junk = db.Column(db.String)
    byline_person_0_firstname = db.Column(db.String)
    byline_person_0_lastname = db.Column(db.String)
    byline_person_0_middlename = db.Column(db.String)
    dominant_topic_name = db.Column(db.String)
    total_articles = db.Column(db.Integer)

    def __init__(self, author):
        """"""
        self.author = author
        self.author_id = author_id
        self.dominant_topic_name = dominant_topic_name
        self.total_articles = total_articles


    def __repr__(self):
        return self.author


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

    author_id = db.Column(db.String, db.ForeignKey("authors.author_id"))
    author = db.relationship("Author", backref=db.backref(
        "articles", order_by=article_id), lazy=True)  #this might need to be changed to author_id


    def __init__(self, headline_main, pub_date, source, type_of_material, web_url):
        """"""
        self.headline_main = headline_main
        self.pub_date = pub_date
        self.source = source
        self.type_of_material = type_of_material
        self.web_url = web_url
