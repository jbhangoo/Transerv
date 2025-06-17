""" survey_form.py """
from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, TimeField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class SurveyForm(FlaskForm):
    project = SelectField('Project', coerce=int, validators=[DataRequired()])
    site = IntegerField('Site', validators=[DataRequired()])
    survey_date = DateField('Survey Date', format='%Y-%m-%d', validators=[DataRequired()])
    time_start = TimeField('Start Time', validators=[DataRequired()])
    time_end = TimeField('End Time')
    observer_count = IntegerField('Number of Observers')
    comments = TextAreaField('Comments')
    submit = SubmitField('Create Survey')
