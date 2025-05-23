"""
Module Name: reports
Description: This module contains routes that generate reports
"""
import json
from sqlalchemy.orm import joinedload

from flask import Blueprint, render_template, request, flash
from forms.site_form import SiteForm
from forms.project_form import ProjectReportForm
from forms.survey_form import SurveyForm

from models.data import db, Project, Site, Observation, Survey
from util.form import form_submit_error_response

# Null chart data to avoid errors
chart_data={'files': [], 'layout': {}}
report_bp = Blueprint('report', __name__, url_prefix='/reports')

@report_bp.route('/project', methods=['GET', 'POST'])
def project_report():
    """
    Project Report
    :return:
    """
    form = ProjectReportForm()
    form.project.choices = [(project.id, project.name)
                            for project in Project.query.order_by('name')]
    form.project.choices.insert(0, (0, 'Choose project'))

    error_response = form_submit_error_response(form, 'reports/project.html',
                                                current_project=None,
                                                observations=[],
                                                species_data="[]",
                                                chart_data="[]",
                                                current_site=request.args.get('site')
                                                )
    if error_response:
        # If GET request or form not valid, just render the initial page
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}", "danger")
        return error_response


    project_id = form.project.data  # Get selected project

    # Query observations based on the selected species
    obs_stmt = db.select(Observation).join(Survey).filter_by(project_id=project_id)
    observations = db.session.execute(obs_stmt).scalars().all()

    # Process files for chart and table
    processed_data = process_observations(observations)
    chart_json = json.dumps(processed_data)  # Convert processed files to JSON for the chart

    return render_template('reports/project.html',
                           form=form,
                           current_project=project_id,
                           observations=observations,
                           species_data=processed_data,
                           chart_data=chart_json,
                           current_site=request.args.get('site')
                           )


def process_observations(observations:list[Observation]):
    """
    Implement your logic to process observations and prepare files for the chart
    Example: Count occurrences, summarize files, etc.
    :param observations:
    :return:
    """
    data = []
    for obs in observations:
        data.append({
            'count': obs.count,
            'count_supp': obs.count_supplemental,
            'behavior': obs.behavior,
            'comments': obs.comments
        })
    return data

@report_bp.route('/sites_map')
def sites_map():
    """

    :return:
    """
    projects = Project.query.order_by('name')
    return render_template('reports/map.html', projects=projects)
