from flask import Flask, request
from models import db

app = Flask(__name__)

POSTGRES = {
    'user': 'jake',
    'pw': 'passwordjake',
    'db': 'newsclusters',
    'host': 'localhost',
    'port': '5432',
}

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jake:passwordjake@localhost:5432/newsclusters'
db.init_app(app)


@app.route('/')
def main():
    return 'Hello Snakers!'


@app.route('/', methods=['GET', 'POST'])
def index():
    search = MusicSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
 
    return render_template('index.html', form=search)





if __name__ == '__main__':
    app.run()