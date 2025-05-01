from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required, current_user

from models.data import db, Project, Site, ProjectSite

projectsite_bp = Blueprint('projectsites', __name__, url_prefix='/projectsites')


@projectsite_bp.route('/', methods=['GET'])
def projectsite_index():
    projects = Project.query.all()
    sites = Site.query.all()
    return render_template('project/projectsites.html', current_user=current_user, projects=projects, sites=sites)

@projectsite_bp.route('/list', methods=['GET', 'POST'])
def projectsite_list():
    # Logic to retrieve all species projects
    projectsites = ProjectSite.query.join(Project).join(Site).with_entities(
        ProjectSite.id,
        Project.name.label('project'),
        Site.name.label('site'),
    ).all()
    return jsonify({'projectsites': [{'id': sp.id, 'project': sp.project, 'site': sp.site} for sp in projectsites]})

# Add a new ProjectSite entry
@projectsite_bp.route('/add', methods=['POST'])
def projectsite_add():
    project_id = request.form.get('project_id')
    site_id = request.form.get('site_id')
    new_projectsite = ProjectSite(project_id=project_id, site_id=site_id)
    db.session.add(new_projectsite)
    db.session.commit()
    # Logic to save new_project to database
    return jsonify({'message': f'ProjectSite "{project_id}, {site_id}" added'}), 201

# Edit an existing ProjectSite entry
@projectsite_bp.route('/edit/<int:id>', methods=['PUT'])
def projectsite_edit(id):
    data = request.json
    # Logic to find project by id and update it
    projectsite = ProjectSite.query.get(id)
    if projectsite.project_id != data['project_id']:
        projectsite.project_id = data['project_id']
    if projectsite.site_id != data['site_id']:
        projectsite.site_id = data['site_id']

    db.session.commit()
    return jsonify({'message': 'ProjectSite {projectsite.id} updated'})

# Delete a ProjectSite entry
@projectsite_bp.route('/delete/<int:id>', methods=['DELETE'])
def projectsite_delete(id):
    # Logic to find project by id and delete it
    projectsite = ProjectSite.query.get(id)
    db.session.delete(projectsite)
    return jsonify({'message': f'ProjectSite {projectsite.id} deleted'})