from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import DataRequired, Optional
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
import pandas as pd
import pytz
from form import SearchForm
from models import db,Task


app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

data_df = pd.read_excel('result_mod_30June2024.xlsx')



@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    patents = []
    message = ""
    total_applicants = 0
    applicants_all = []
    applicants_exclude_large = []
    
    if form.validate_on_submit():
        keyword = form.keyword.data
        filtered_data = data_df[data_df['title'].str.contains(keyword, case=False)]

        if filtered_data.empty:
            message = "해당 검색어에 대한 특허를 찾을 수 없습니다"
        else:
            top_10_patents = filtered_data.head(10).to_dict(orient='records')
            applicant_counts_all = filtered_data.groupby('applicant').size().reset_index(name='count')
            applicants_all = applicant_counts_all.sort_values(by='count', ascending=False).head(5).to_dict(orient='records')
            applicants = filtered_data['applicant'].tolist()
            total_applicants = len(set(applicants))
            filtered_applicants = filtered_data[filtered_data['applicant_lgrp'] == '국내기업']
            applicant_counts_exclude_large = filtered_applicants.groupby('applicant').size().reset_index(name='count')
            applicants_exclude_large = applicant_counts_exclude_large.sort_values(by='count', ascending=False).head(5).to_dict(orient='records')
            patents = top_10_patents

    return render_template('index.html', form=form, patents=patents, message=message, total_applicants=total_applicants, applicants_all=applicants_all, applicants_exclude_large=applicants_exclude_large)

if __name__ == '__main__':
    app.run(debug=True)


