# forms.py
 
from wtforms import Form, StringField, SelectField, validators
 
class ReporterSearchForm(Form):
    choices = [('author', 'Reporter Name'),
               ('headline_main', 'Headline'),
               ('dominant_topic_name', 'Topic')]
    select = SelectField('Search for Reporters Using:', choices=choices)
    search = StringField('')