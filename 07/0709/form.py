from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, IntegerField
from wtforms.validators import DataRequired, Optional

class SearchForm(FlaskForm):
    filter = StringField('필터',validators=[Optional()])
    keyword =StringField('검색어',validators=[Optional()])
    applicate_date = DateField('출원일자',validators=[Optional()],format='%Y-%m-%d')