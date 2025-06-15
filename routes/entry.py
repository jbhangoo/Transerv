"""
Module Name: entry
Description: This module contains routes related to survey entries.
"""

from flask import Blueprint, render_template, redirect, request, jsonify, url_for, flash, current_app
from flask_login import login_required, current_user

from handlers.decorators import role_required
from models.data import db, UserRole, Site, Survey, Observation, Species, Project, ProjectSite
from forms.survey_form import SurveyForm
from forms.observation_form import ObservationForm
from util.form import form_submit_error_response

entry_bp = Blueprint('entry', __name__, url_prefix='/entry')

@entry_bp.route('/survey/list', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.MEMBER)
def survey_list():
    """
    Function Name: survey_list
    Description: Lists all surveys.
    """
    all_surveys = Survey.query\
                .order_by('project_id', 'name', 'survey_date', 'time_start')\
                .join(Site)\
                .with_entities(Survey.id, Site.name, Survey.survey_date,
                              Survey.time_start, Survey.time_end,
                              Survey.observer_count, Survey.comments).all()
    print("survey_list", all_surveys)
    return jsonify({'surveys':
                        [{
                            'id': survey.id,
                            'site': survey.name,
                            'survey_date': survey.survey_date.isoformat(),
                            'time_start': survey.time_start.isoformat(),
                            'time_end': survey.time_end.isoformat(),
                            'observer_count': survey.observer_count,
                            'comments': survey.comments}
                         for survey in all_surveys]})

@entry_bp.route('/survey_add', methods=['POST'])
@login_required
@role_required(UserRole.MEMBER)
def survey_add():
    """
    Function Name: survey_add
    Description: Adds a new survey.
    """
    project = request.form.get('project')
    project = int(project)
    pr_site_id = request.form.get('site')
    prsite = ProjectSite.query.get(pr_site_id)
    site = prsite.site_id

    if (not site) or (site == '0'):
        return jsonify({'message': 'Site is required'}), 400

    site = int(site)

    survey_date = request.form.get('survey_date')
    if not survey_date:
        return jsonify({'message': 'Survey date is required'}), 400

    time_start = request.form.get('time_start')
    time_end = request.form.get('time_end')
    if time_end <= time_start:
        return jsonify({'message':
                        f'Start time ({time_start}) must be before end time ({time_end})'}), 400
    observer_count = request.form.get('observer_count')
    if not observer_count:
        observer_count = 0
    else:
        observer_count = int(observer_count)
    comments = request.form.get('comments')
    current_app.logger.info(f"Adding SURVEY: User {current_user.id}, Project {project}, "
          f"Site {site}, {survey_date}, {time_start}, {time_end}, "
          f"nobs={observer_count}, comments= '{comments}'")
    new_survey = Survey(user_id=current_user.id, project_id=project,
                        site_id=site, survey_date=survey_date,
                        time_start=time_start, time_end=time_end,
                        observer_count=observer_count, comments=comments)
    db.session.add(new_survey)
    db.session.commit()
    return jsonify({'message': f'Survey "{survey_date}" added'}), 201

@entry_bp.route('/surveys', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.MEMBER)
def surveys():
    """
    Function Name: surveys
    Description: Allows the user to manage surveys.
    """
    projects = Project.query.order_by('name')
    return render_template('entry/surveys.html', projects=projects)

@entry_bp.route('/survey_edit/<int:survey_id>', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.MEMBER)
def survey_edit(survey_id):
    """
    Function Name: survey_edit
    Description: Edits an existing survey.
    """
    survey = Survey.query.get(survey_id)
    project = Project.query.get(survey.project_id)

    form = SurveyForm()

    newform = SurveyForm(data=form.data)
    newform.project.choices = [(proj.id, proj.name) for proj in Project.query.order_by('name')]
    newform.project.choices.insert(0, (0, 'Choose project'))
    newform.project.data = survey.project_id
    newform.site.choices = [(site.id, site.name)
                            for site in ProjectSite.query.filter_by(project_id=project.id or 0)
                            .join(Site).with_entities(Site.id, Site.name).all()]
    newform.site.choices.insert(0, (0, 'Choose site'))
    newform.site.data = survey.site_id
    newform.survey_date.data = survey.survey_date
    newform.time_start.data = survey.time_start
    newform.time_end.data = survey.time_end
    newform.observer_count.data = survey.observer_count
    newform.comments.data = survey.comments

    recent_surveys = (Survey.query
                      .filter_by(user_id=current_user.id)
                      .order_by(Survey.survey_date.desc())
                      .limit(5).all())
    error_response = form_submit_error_response(newform, 'entry/survey_edit.html',
                                                survey_id=survey_id, recent_surveys=recent_surveys)
    if error_response:
        return error_response

    # Update the Survey object with the form files if different
    if survey.project_id != form.project.data:
        survey.project_id = form.project.data

    if survey.site_id != form.site.data:
        survey.site_id = form.site.data

    if survey.survey_date != form.survey_date.data:
        survey.survey_date = form.survey_date.data

    if survey.time_start != form.time_start.data:
        survey.time_start = form.time_start.data

    if survey.time_end != form.time_end.data:
        survey.time_end = form.time_end.data

    if survey.observer_count != form.observer_count.data:
        survey.observer_count = form.observer_count.data

    if survey.comments != form.comments.data:
        survey.comments = form.comments.data

    # Validate end_date > start_date
    if survey.time_end <= survey.time_start:
        flash("End must be after start", "error")
        return render_template('entry/survey_edit.html',
                               form=form, survey_id=survey_id, recent_surveys=recent_surveys)

    db.session.commit()
    flash('Survey Updated!')
    return render_template('entry/survey_edit.html',
                           form=form, survey_id=survey_id, recent_surveys=recent_surveys)

@entry_bp.route('/observation_add/<int:survey_id>/', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.MEMBER)
def observation_add(survey_id):
    """
    Function Name: observation_add
    Description: Add a new observation to a survey.
    :param survey_id:   Survey to add observation to
    :return:
    """
    project_id = Survey.query.get(survey_id).project_id
    species_id = Project.query.get(project_id).species_id

    form = ObservationForm()
    form.survey_id.data = survey_id
    form.species_id.choices = [(species.id, species.common_name)
                               for species in Species.query.order_by('common_name')]
    form.species_id.choices.insert(0, (0, 'Choose species'))
    form.species_id.data = species_id or 0


    # join Species to get common name
    results = (db.session.query(Observation)
               .filter(Observation.survey_id == survey_id)
               .join(Species)
               .all())
    error_response = form_submit_error_response(form, 'entry/observation_add.html',
                                                survey_id=survey_id, observations=results)
    if error_response:
        return error_response

    # Validate there is a count
    if (form.count.data is None or form.count.data <= 0) and (form.count_supplemental.data is None or form.count_supplemental.data <= 0):
        flash("Either count or count supplemental must be entered and positive", "error")
        return render_template('entry/observation_add.html',
                               form=form, survey_id=survey_id, observations=results)

    obs = Observation(
        survey_id=form.survey_id.data,
        species_id=form.species_id.data,
        count=form.count.data,
        count_supplemental=form.count_supplemental.data,
        latitude=form.latitude.data,
        longitude=form.longitude.data,
        direction=form.direction.data,
        behavior=form.behavior.data,
        comments=form.comments.data
    )
    db.session.add(obs)
    db.session.commit()
    flash('Observation added! Add another?')
    return redirect(url_for('entry.observation_add', survey_id=survey_id, observations=results))

@entry_bp.route('/observation_edit/<int:observation_id>', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.MEMBER)
def observation_edit(observation_id):
    """
    Function Name: observation_edit
    Description: Allows the user to edit the observation
    :param observation_id: Observation to edit
    :return:
    """
    form = ObservationForm()
    results = db.session.query(Observation)\
               .filter(Observation.id == observation_id)\
               .join(Species).first()

    newform = ObservationForm(data=form.data)
    newform.species_id.choices = [(species.id, species.common_name)
                                  for species in Species.query.order_by('common_name')]
    newform.survey_id.data = results.survey_id
    newform.count.data = results.count
    newform.count_supplemental.data = results.count_supplemental
    newform.latitude.data = results.latitude
    newform.longitude.data = results.longitude
    newform.direction.data = results.direction
    newform.behavior.data = results.behavior
    newform.comments.data = results.comments

    error_response = form_submit_error_response(newform, 'entry/observation_edit.html',
                                                observation_id=observation_id,
                                                survey_id=results.survey_id)
    if error_response:
        return error_response

    # Update the Observation object with the form files if different
    obs = Observation.query.get(observation_id)
    if obs.species_id !=form.species_id.data:
        obs.species_id = form.species_id.data

    if obs.count != form.count.data:
        obs.count = form.count.data

    if obs.count_supplemental != form.count_supplemental.data:
        obs.count_supplemental = form.count_supplemental.data

    if obs.direction != form.direction.data:
        obs.direction = form.direction.data

    if obs.behavior != form.behavior.data:
        obs.behavior = form.behavior.data

    if obs.comments != form.comments.data:
        obs.comments = form.comments.data

    if obs.latitude != form.latitude.data:
        obs.latitude = form.latitude.data
    if obs.longitude != form.longitude.data:
        obs.longitude = form.longitude.data

    db.session.commit()
    flash('Observation Updated!')
    return redirect(url_for('entry.observation_edit',
                            form=obs,
                            observation_id=observation_id,
                            survey_id=obs.survey_id))

@entry_bp.route('/observation_delete/<int:observation_id>/<int:survey_id>', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.MEMBER)
def observation_delete(observation_id, survey_id):
    """
    Function Name: observation_delete
    Description: Allows the user to delete the observation
    :param observation_id:  Observation to be deleted
    :param survey_id:       Needed to setup next page after deletion is done
    :return:
    """
    results = (db.session.query(Observation)
               .filter(Observation.id == observation_id)
               .join(Species).all())

    obs = Observation.query.get(observation_id)
    db.session.delete(obs)
    db.session.commit()
    flash('Observation deleted successfully.')
    return redirect(url_for('entry.observation_add',
                            form=obs, survey_id=survey_id, observations=results))
