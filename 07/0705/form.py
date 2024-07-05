from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, IntegerField
from wtforms.validators import DataRequired

class SearchTask(FlaskForm):
    filter = StringField('필터')
    keyword =TextAreaField('검색어')
    applicate_date = DateField('출원일자')