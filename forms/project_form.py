""" project_form.py """
from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, SubmitField, StringField
from wtforms.validators import DataRequired

class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired()])
    description = StringField('Description')
    species_id = SelectField('Species', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')

class ProjectReportForm(FlaskForm):
    # ... dynamically populated via AJAX
    project = SelectField('Project', coerce=int, validators=[DataRequired()])
    date_start = DateField('Start Date', format='%Y-%m-%d')
    date_end = DateField('End Date', format='%Y-%m-%d')

    submit = SubmitField('See Species')
