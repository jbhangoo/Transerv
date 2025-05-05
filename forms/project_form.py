from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, SubmitField
from wtforms.validators import DataRequired

class ProjectReportForm(FlaskForm):
    # ... dynamically populated via AJAX
    project = SelectField('Project', coerce=int, validators=[DataRequired()])
    site = SelectField('Site', coerce=int,  validators=[DataRequired()])
    date_start = DateField('Start Date', format='%Y-%m-%d')
    date_end = DateField('End Date', format='%Y-%m-%d')

    submit = SubmitField('See Species')
