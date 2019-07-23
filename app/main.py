# main.py

from app import app
from db_setup import init_db, db_session
from forms import ReporterSearchForm
from flask import flash, render_template, request, redirect
from models import Article, Author
from tables import Results

init_db()


@app.route('/', methods=['GET', 'POST'])
def index():
    search = ReporterSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('index.html', form=search)


@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']

    if search_string:
        if search.data['select'] == 'author':
            qry = db_session.query(Article, Author).filter(
                Author.author_id==Article.author_id).filter(
                    Author.author.contains(search_string))
            results = [item[0] for item in qry.all()]
        elif search.data['select'] == 'headline_main':
            qry = db_session.query(Article).filter(
                Article.headline_main.contains(search_string))
            results = qry.all()
        else:
            qry = db_session.query(Article)
            results = qry.all()
    else:
        qry = db_session.query(Article)
        results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)









if __name__ == '__main__':
    import os
    if 'WINGDB_ACTIVE' in os.environ:
        app.debug = False
    app.run(port=5001)