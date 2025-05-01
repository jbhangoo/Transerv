# WTForms with dynamic location selection
from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, TimeField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import NumberRange, DataRequired

class LocationForm(FlaskForm):
    # ... dynamically populated via AJAX
    location = SelectField('Location', coerce=int)

    submit = SubmitField('See Location')


