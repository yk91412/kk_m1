from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
import pytz
from form import SearchForm
from models import db,Task

app = Flask(__name__)
app.config.from_pyfile('config.py')


db.init_app(app)
migrate = Migrate(app,db)
csrf = CSRFProtect(app)




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        keyword = form.keyword.data
        # 데이터베이스에서 검색어와 관련된 특허 조회
        patents = Task.query.filter(or_(Task.title.ilike(f'%{keyword}%'),
                                          Task.summary.ilike(f'%{keyword}%'))).all()
        return render_template('search_results.html', patents=patents, keyword=keyword)
    return render_template('search.html', form=form)

@app.route('/results')
def results():
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)