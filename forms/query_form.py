""" query_form.py """
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class QueryForm(FlaskForm):
    input_text = TextAreaField('Input', validators=[DataRequired()])
    submit = SubmitField('Submit')
