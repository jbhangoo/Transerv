from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, TimeField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import NumberRange, DataRequired

class SurveyForm(FlaskForm):
    project = SelectField('Project', coerce=int)
    site = IntegerField('Site', validators=[DataRequired()])
    survey_date = DateField('Survey Date', format='%Y-%m-%d', validators=[DataRequired()])
    time_start = TimeField('Start Time', validators=[DataRequired()])
    time_end = TimeField('End Time')
    observer_count = IntegerField('Number of Observers', validators=[NumberRange(min=1, max=20)])
    comments = TextAreaField('Comments')
    submit = SubmitField('Create Survey')
