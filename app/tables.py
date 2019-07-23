from flask_table import Table, Col
 
class Results(Table):
    article_id = Col('Article Id', show=False)
    author = Col('Author')
    headline_main = Col('Headline')
    pub_date = Col('Publication Date')
    byline_person_0_lastname = Col('Last Name')