from flask_table import Table, Col
 
class Results(Table):
    article_id = Col('Article Id', show=False)
    author = Col('Author')
    headline_main = Col('Headline')
    topic_name = Col('Topic')
    pub_date = Col('Publication Date')

    type_of_material = Col('Type of Article')
    web_url = Col('URL')

#finish this later
class ByAuthorDetailsResults(Table):
    author = Col('Author')
    dominant_topic_name = Col('dominant_topic_name')

