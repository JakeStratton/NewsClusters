from flask import Flask, request, flash, render_template, request, redirect
from models import db
from forms import ReporterSearchForm


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
app.config['SECRET_KEY'] = 'you-will-never-guess'
db.init_app(app)


@app.route('/')
def main():
    return 'Hello Jake S!'



@app.route('/index', methods=['GET', 'POST'])
def index():
    search = ReporterSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
 
    return render_template('index.html', form=search)




@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']
 
    if search.data['search'] == '':
        qry = db_session.query(Articles)
        results = qry.all()
 
    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('results.html', results=results)



if __name__ == '__main__':
    app.run()