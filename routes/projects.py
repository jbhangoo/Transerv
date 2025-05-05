from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user

from models.data import db, Project, Species

project_bp = Blueprint('project', __name__, url_prefix='/project')


@project_bp.route('/', methods=['GET'])
def project_index():
    species = Species.query.all()
    return render_template('project/projects.html',
                           current_user=current_user, species=species)
@project_bp.route('/list', methods=['GET', 'POST'])
def project_list():
    # Logic to retrieve all species projects
    projects = Project.query.all()
    return jsonify({'projects':
                        [{
                            'id': sp.id,
                            'name': sp.name,
                            'description': sp.description,
                            'species_code': sp.species_code}
                         for sp in projects]})

# Add a new Project entry
@project_bp.route('/add', methods=['POST'])
def project_add():
    name = request.form.get('name')
    description = request.form.get('description')
    species_code = request.form.get('species_code')
    new_project = Project(name=name, description=description, species_code=species_code)
    db.session.add(new_project)
    db.session.commit()
    # Logic to save new_project to database
    return jsonify({'message': f'Project "{name}" added'}), 201

# Edit an existing Project entry
@project_bp.route('/edit/<int:projectid>', methods=['PUT'])
def project_edit(projectid):
    data = request.json
    # Logic to find project by id and update it
    project = Project.query.get(projectid)
    if project.name != data['name']:
        project.name = data['name']
    if project.description != data['description']:
        project.description = data['description']
    if project.species_code != data['species_id']:
        project.species_code = data['species_id']

    db.session.commit()
    return jsonify({'message': 'Project updated'})

# Delete a Project entry
@project_bp.route('/delete/<int:projectid>', methods=['DELETE'])
def project_delete(projectid):
    # Logic to find project by id and delete it
    project = Project.query.get(projectid)
    db.session.delete(project)
    return jsonify({'message': f'Project {project.name} deleted'})