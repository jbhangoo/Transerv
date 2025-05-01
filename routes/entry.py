from flask import Blueprint, render_template, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

from decorators import role_required
from models.data import db, UserRole, Site, Location, Survey, Observation, Species, Project, ProjectSite
from forms.survey import SurveyForm
from forms.observation import ObservationForm
from util.form import form_submit_error_response
entry_bp = Blueprint('entry', __name__, url_prefix='/entry')


@entry_bp.route('/survey_add', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.MEMBER)
def survey_add():
    form = SurveyForm()
    form.location.choices = [(loc.id, loc.name) for loc in Location.query.order_by('name')]
    form.location.choices.insert(0, (0, 'Choose location'))
    form.project.choices = [(proj.id, proj.name) for proj in Project.query.order_by('name')]
    form.project.choices.insert(0, (0, 'Choose project'))

    recent_surveys = Survey.query.filter_by(user_id=current_user.id).order_by(Survey.survey_date.desc()).limit(5).all()
    error_response = form_submit_error_response(form, 'entry/survey_add.html', recent_surveys=recent_surveys)
    if error_response:
        return error_response

    survey = Survey(
        user_id=current_user.id,
        project_id=form.project.data,
        site_id=form.site.data,
        survey_date=form.survey_date.data,
        time_start=form.time_start.data,
        time_end=form.time_end.data,
        observer_count=form.observer_count.data,
        comments=form.comments.data
    )
    db.session.add(survey)
    db.session.commit()

    # Go directly to the observations entry form
    return redirect(url_for('entry.observation_add', survey_id=survey.id))


@login_required
@entry_bp.route('/survey_edit/<int:survey_id>', methods=['GET', 'POST'])
def survey_edit(survey_id):
    survey = Survey.query.get(survey_id)
    if survey and survey.site:
        if survey.site.location_id:
            location = Location.query.get(survey.site.location_id)
            project = Project.query.first()
        else:
            location = Location.query.first()
            project = Project.query.first()
    elif survey.project_id:
        location = Location.query.first()
        project = Project.query.get(survey.project_id)
    else:
        location = Location.query.first()
        project = Project.query.first()

    form = SurveyForm()
    form.location.choices = [(loc.id, loc.name) for loc in Location.query.order_by('name')]
    form.project.choices = [(proj.id, proj.name) for proj in Project.query.order_by('name')]
    form.site.choices = [(site.id, site.name) for site in
                         ProjectSite.query.filter_by(project_id=project.id or 0).join(Site).with_entities(Site.id, Site.name).all()]

    newform = SurveyForm(data=form.data)
    newform.location.choices = [(loc.id, loc.name) for loc in Location.query.order_by('name')]
    newform.project.choices = [(proj.id, proj.name) for proj in Project.query.order_by('name')]
    newform.site.choices = [(site.id, site.name) for site in
                         Site.query.filter_by(location_id=location.id or 0)]
    newform.location.data = location.id
    newform.site.data = survey.site_id
    newform.survey_date.data = survey.survey_date
    newform.time_start.data = survey.time_start
    newform.time_end.data = survey.time_end
    newform.observer_count.data = survey.observer_count
    newform.comments.data = survey.comments

    recent_surveys = Survey.query.filter_by(user_id=current_user.id).order_by(Survey.survey_date.desc()).limit(5).all()
    error_response = form_submit_error_response(newform, 'entry/survey_edit.html', survey_id=survey_id, recent_surveys=recent_surveys)
    if error_response:
        return error_response

    # Update the Survey object with the form data if different
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
        return render_template('entry/survey_edit.html', form=form, survey_id=survey_id, recent_surveys=recent_surveys)

    db.session.commit()
    flash('Survey Updated!')
    return redirect(url_for('entry.observation_add', survey_id=survey.id, observations=survey.observations))


@entry_bp.route('/observation_add/<int:survey_id>/', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.MEMBER)
def observation_add(survey_id):
    form = ObservationForm()
    form.survey_id.data = survey_id
    form.species_id.choices = [(species.id, species.common_name) for species in Species.query.order_by('common_name')]

    # join Species to get common name
    results = db.session.query(Observation, Species).outerjoin(Species, Observation.species_id == Species.id) \
    .filter(Observation.survey_id == survey_id).all()
    error_response = form_submit_error_response(form, 'entry/observation_add.html', survey_id=survey_id, observations=results)
    if error_response:
        return error_response

    obs = Observation(
        survey_id=form.survey_id.data,
        species_id=form.species_id.data,
        count=form.count.data,
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
    form = ObservationForm()
    results = db.session.query(Observation, Species).outerjoin(Species, Observation.species_id == Species.id) \
    .filter(Observation.id == observation_id).all()

    robs, rspecies = results[0]

    newform = ObservationForm(data=form.data)
    newform.species_id.choices = [(species.id, species.common_name) for species in Species.query.order_by('common_name')]
    newform.survey_id.data = robs.survey_id
    newform.count.data = robs.count
    newform.count_supplemental.data = robs.count_supplemental
    newform.behavior.data = robs.behavior
    newform.comments.data = robs.comments

    error_response = form_submit_error_response(newform, 'entry/observation_edit.html', observation_id=observation_id, survey_id=robs.survey_id, observations=results)
    if error_response:
        return error_response

    # Update the Observation object with the form data if different
    obs = Observation.query.get(observation_id)
    if obs.species_id !=form.species_id.data:
        obs.species_id = form.species_id.data

    if obs.count != form.count.data:
        obs.count = form.count.data

    if obs.count_supplemental != form.count_supplemental.data:
        obs.count_supplemental = form.count_supplemental.data

    if obs.behavior != form.behavior.data:
        obs.behavior = form.behavior.data

    if obs.comments != form.comments.data:
        obs.comments = form.comments.data

    db.session.commit()
    flash('Observation Updated!')
    return redirect(url_for('entry.observation_edit', form=obs, observation_id=observation_id, survey_id=obs.survey_id, observations=results))


@entry_bp.route('/observation_delete/<int:observation_id>/<int:survey_id>', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.MEMBER)
def observation_delete(observation_id, survey_id):
    results = db.session.query(Observation, Species).outerjoin(Species, Observation.species_id == Species.id) \
    .filter(Observation.id == observation_id).all()

    obs = Observation.query.get(observation_id)
    db.session.delete(obs)
    db.session.commit()
    flash('Observation deleted successfully.')
    return redirect(url_for('entry.observation_add', form=obs, survey_id=survey_id, observations=results))
