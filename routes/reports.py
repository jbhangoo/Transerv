import json
from sqlalchemy.orm import joinedload

from flask import Blueprint, render_template, request, flash
from forms.site_form import SiteForm
from forms.project_form import ProjectReportForm
from forms.survey_form import SurveyForm

from models.data import db, Project, Site, Observation

"""Fix this later"""
chart_data={'data': [], 'layout': {}}
report_bp = Blueprint('report', __name__, url_prefix='/reports')


@report_bp.route('/project', methods=['GET', 'POST'])
def project_report():
    print("Request Method:", request.method)
    print("Form Data:", request.form)

    form = ProjectReportForm()
    form.project.choices = [(project.id, project.name)
                            for project in Project.query.order_by('name')]
    form.project.choices.insert(0, (0, 'Choose project'))

    if form.validate_on_submit():
        project_id = form.project.data  # Get selected species code

        # Query observations based on the selected species
        obs_stmt = db.select(Observation).filter_by(project_id=project_id)
        observations = db.session.execute(obs_stmt).scalars().all()

        # Process data for chart and table
        processed_data = process_observations(observations)
        chart_json = json.dumps(processed_data)  # Convert processed data to JSON for the chart

        return render_template('reports/project.html',
                               form=form,
                               current_project=project_id,
                               observations=observations,
                               species_data=processed_data,
                               chart_data=chart_json,
                               current_site=request.args.get('site')
                               )

    # If GET request or form not valid, just render the initial page
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in {field}: {error}", "danger")
    return render_template('reports/project.html',
                           form=form,
                           current_project=None,
                           observations=[],
                           species_data="[]",
                           chart_data="[]",
                           current_site=request.args.get('site')
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

@report_bp.route('/site')
def site_report():
    form = SiteForm()
    sites = Site.query.all()
    return render_template('reports/sites.html',
                           form=form, sites=sites, chart_data=chart_data)


@report_bp.route('/surveys')
def survey_report():
    form = SurveyForm()
    projects = Project.query.all()
    surveys = Site.query.options(
        joinedload(Site.surveys)
    ).all()
    return render_template('reports/surveys.html',
                           form=form, projects=projects, surveys=surveys, chart_data=chart_data)

@report_bp.route('/sitemap')
def sitemap():
    return render_template('reports/map.html')
