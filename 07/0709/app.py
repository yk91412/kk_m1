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
import pandas as pd


app = Flask(__name__)
app.config.from_pyfile('config.py')


db.init_app(app)
migrate = Migrate(app,db)
csrf = CSRFProtect(app)

data_df = pd.read_excel('result_mod_30June2024.xlsx')

@app.route('/')
def index():
    form = SearchForm()
    return render_template('index.html',form=form)



@app.route('/search', methods=['POST'])
def search():    
    form=SearchForm()
    if form.validate_on_submit():
        keyword = form.keyword.data
        filtered_data = data_df[data_df['title'].str.contains(keyword, case=False)]

        if filtered_data.empty:
            return render_template('search_results.html',patents=[],message="해당 검색어에 대한 특허를 찾을 수 없습니다")
            
    
    # 상위 10개의 데이터를 가져옴
        top_10_patents = filtered_data.head(10).to_dict(orient='records')

        # 출원인 전체 목록

        applicant_counts_all = filtered_data.groupby('applicant').size().reset_index(name='count')
        applicants_all = applicant_counts_all.sort_values(by='count',ascending=False).head(5).to_dict(orient='records')

        # 출원인 수
        applicants = filtered_data['applicant'].tolist()

        total_applicants = len(set(applicants))
        # 대기업 제외 출원인 목록
        filtered_applicants = filtered_data[filtered_data['applicant_lgrp'] == '국내기업']
        applicant_counts_exclude_large = filtered_applicants.groupby('applicant').size().reset_index(name='count')
        applicants_exclude_large = applicant_counts_exclude_large.sort_values(by='count',ascending=False).head(5).to_dict(orient='records')

        
        # top_5_applicants = filtered_data['applicant'].value_counts().sort_values(ascending=False).head(5)
        # filtered_df = filtered_data[filtered_data['applicant_lgrp'] == '국내기업']
        # top_5_non_big_applicants = filtered_df['applicant'].value_counts().sort_values(ascending=False).head(5)

        return render_template('search_results.html', patents=top_10_patents, applicants_all=applicants_all, applicants_exclude_large=applicants_exclude_large, total_applicants=total_applicants)


    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)