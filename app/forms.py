# forms.py
 
from wtforms import Form, StringField, SelectField
 
class ReporterSearchForm(Form):
    choices = [('author', 'Reporter Name'),
               ('text', 'Text')]
    select = SelectField('Search for reporters:', choices=choices)
    search = StringField('')