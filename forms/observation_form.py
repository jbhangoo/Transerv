from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange, ValidationError, Optional

class ObservationForm(FlaskForm):
    survey_id = IntegerField('survey id', validators=[NumberRange(min=1)])
    species_id = SelectField('Species', coerce=int, validators=[DataRequired()])
    count = IntegerField('Count', validators=[Optional()])
    count_supplemental = IntegerField('Count Supplemental', validators=[Optional()])
    behavior = SelectField('Behavior', choices=[
        ('', 'Select'),
        ('foraging', 'Foraging'),
        ('nesting', 'Nesting'),
        ('flying', 'Flying')
    ])
    comments = TextAreaField('Comments')
    submit = SubmitField('Add Observation')

    def validate_count(self, field):
        if field.data and field.data < 0:
            raise ValidationError('If you enter a count it must be a positive number')
