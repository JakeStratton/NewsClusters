from app import db

class Article(db.Model):
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


    def __init__(self, name, author, published):
        self.headline_main = headline_main
        self.author = author
        self.author_id = author_id
        self.pub_date = pub_date
        self.section_name = section_name
        self.source = source
        self.type_of_material = type_of_material
        self.web_url = web_url
        self.word_count = word_count
        self.text = text

    def __repr__(self):
        return '<article_id {}>'.format(self.article_id)
    
    def serialize(self):
        return {
            'article_id': self.article_id, 
            'headline_main': self.headline_main,
            'author': self.author,
            'author_id':self.author_id,
            'pub_date': self.pub_date, 
            'section_name': self.section_name,
            'source': self.source,
            'type_of_material':self.type_of_material,
            'web_url': self.web_url, 
            'word_count': self.word_count,
            'text': self.text                      
        }