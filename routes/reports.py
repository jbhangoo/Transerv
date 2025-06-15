"""
Module Name: reports
Description: This module contains routes that generate reports
"""
import json

from flask import Blueprint, render_template, request, flash
from forms.project_form import ProjectReportForm

from models.data import db, Project, Site, ProjectSite, Observation, Survey, Species
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
                                                species_data=[],
                                                chart_data='[]',
                                                current_site=request.args.get('site')
                                                )
    if error_response:
        # If GET request or form not valid, just render the initial page
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}", "danger")
        return error_response

    if form.project.data:
        project_id = form.project.data

        # Query observations based on the selected species
        obs_stmt = (db.select(
            Survey.survey_date,
            Species.common_name,
            Site.name,
            Observation.latitude,
            Observation.longitude,
            Observation.count,
            Observation.count_supplemental,
            Observation.direction,
            Observation.behavior,
            Observation.comments,
        )
                    .select_from(Survey)
                    .join(Observation, Survey.id == Observation.survey_id)
                    .join(Site, Survey.site_id == Site.id)
                    .join(Species, Observation.species_id == Species.id)
                    .join(ProjectSite, Site.id == ProjectSite.site_id)
                    .filter(ProjectSite.project_id == project_id)
                    .order_by(Survey.survey_date, Species.common_name)
                    .distinct())
        if form.date_start.data:
            obs_stmt = obs_stmt.filter(Survey.survey_date >= form.date_start.data)
        if form.date_end.data:
            obs_stmt = obs_stmt.filter(Survey.survey_date <= form.date_end.data)
        observations = db.session.execute(obs_stmt).all()

        # Process observations for the chart
        chart_data = {}
        for obs in observations:
            common_name = obs[1]  # common_name is at index 1
            survey_date = obs[0]  # survey_date is at index 0
            count = obs[5] or 0   # count is at index 6
            count_supp = obs[6] or 0  # count_supplemental is at index 7
            total = count + count_supp
            
            if common_name not in chart_data:
                chart_data[common_name] = {
                    'x': [],  # dates
                    'y': [],  # counts
                    'text': []  # hover text
                }
            
            chart_data[common_name]['x'].append(survey_date.isoformat())
            chart_data[common_name]['y'].append(total)
            chart_data[common_name]['text'].append(f"Date: {survey_date.strftime('%Y-%m-%d')}<br>Count: {count}" + 
                                                 (f"<br>Supplemental: {count_supp}" if count_supp > 0 else ""))
    else:
        project_id = None
        observations = []
        chart_data = {}

    # Convert chart data to list of traces for Plotly
    traces = []
    for species, data in chart_data.items():
        traces.append({
            'x': data['x'],
            'y': data['y'],
            'text': data['text'],
            'name': species,
            'type': 'scatter',
            'mode': 'lines+markers',
            'hoverinfo': 'text+name',
            'hovertemplate': '%{text}<extra>%{name}</extra>'
        })
    layout = {
        'title': 'Observations by Species',
        'xaxis': {
            'title': 'Date'
        },
        'yaxis': {
            'title': 'Count'
        }
    }
    chart_data = {'data': traces, 'layout': layout}

    return render_template('reports/project.html',
                           form=form,
                           current_project=project_id,
                           observations=observations,
                           current_site=request.args.get('site'),
                           chart_data=chart_data
                           )


@report_bp.route('/sites_map')
def sites_map():
    """
    Map
    :return:
    """
    projects = Project.query.order_by('name')
    return render_template('reports/map.html', projects=projects)
