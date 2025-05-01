# WTForms with dynamic location selection
from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, TimeField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import NumberRange, DataRequired

class SpeciesReportForm(FlaskForm):
    # ... dynamically populated via AJAX
    species = SelectField('Species', coerce=int, validators=[DataRequired()])
    location = SelectField('Location', coerce=int,  validators=[DataRequired()])
    date_start = DateField('Start Date', format='%Y-%m-%d')
    date_end = DateField('End Date', format='%Y-%m-%d')

    submit = SubmitField('See Species')


