from flask import Blueprint, render_template, request, flash
from forms.species import SpeciesReportForm
from forms.location import LocationForm
from forms.survey import SurveyForm
from sqlalchemy.orm import joinedload
import json

from decorators import role_required
from models.data import db, Site, Location, Species, Observation

"""Fix this later"""
chart_data={'data': [], 'layout': {}}
report_bp = Blueprint('report', __name__, url_prefix='/reports')


@report_bp.route('/species', methods=['GET', 'POST'])
def species_report():
    print("Request Method:", request.method)
    print("Form Data:", request.form)

    form = SpeciesReportForm()
    form.location.choices = [(loc.id, loc.name) for loc in Location.query.order_by('name')]
    form.location.choices.insert(0, (0, 'Choose location'))
    form.species.choices = [(species.id, species.common_name) for species in Species.query.order_by('common_name')]
    form.location.choices.insert(0, (0, 'Choose species'))

    if form.validate_on_submit():
        sp_code = form.species.data  # Get selected species code
        species = Species.query.filter(Species.id == sp_code).first()  # Get species details

        # Query observations based on the selected species
        obs_stmt = db.select(Observation).filter_by(species_id=sp_code)
        observations = db.session.execute(obs_stmt).scalars().all()

        # Process data for chart and table
        processed_data = process_observations(observations)  # Define this function to format your data
        chart_json = json.dumps(processed_data)  # Convert processed data to JSON for the chart

        return render_template('reports/species.html',
                               form=form,
                               current_species=sp_code,
                               observations=observations,
                               species_data=processed_data,
                               chart_data=chart_json,
                               current_location=request.args.get('location')
                               )

    # If GET request or form not valid, just render the initial page
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in {field}: {error}", "danger")
    return render_template('reports/species.html',
                           form=form,
                           current_species=None,
                           observations=[],
                           species_data="[]",
                           chart_data="[]",
                           current_location=request.args.get('location')
                           )


def process_observations(observations):
    # Implement your logic to process observations and prepare data for the chart
    # Example: Count occurrences, summarize data, etc.
    data = []
    for obs in observations:
        data.append({
            'date': obs.date,  # Assuming you have a date field
            'count': obs.count,  # Assuming you have a count field
            # Add more fields as necessary
        })
    return data

@report_bp.route('/location')
def location_report():
    form = LocationForm()
    locations = Location.query.all()
    return render_template('reports/locations.html', form=form, locations=locations, chart_data=chart_data)


@report_bp.route('/surveys')
def survey_report():
    form = SurveyForm()
    locations = Location.query.all()
    surveys = Site.query.options(
        joinedload(Site.surveys)
    ).all()
    return render_template('reports/surveys.html', form=form, locations=locations, surveys=surveys, chart_data=chart_data)

@report_bp.route('/map')
def map():

    return render_template('reports/map.html')