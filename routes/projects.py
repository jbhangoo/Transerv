"""
Module Name: projects
Description: This module contains routes related to project management.
"""

from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required

from handlers.decorators import role_required, UserRole
from models.data import db, Project, Species
from  forms.project_form import ProjectForm
from util.form import form_submit_error_response

project_bp = Blueprint('project', __name__, url_prefix='/projects')


@project_bp.route('/', methods=['GET'])
@login_required
@role_required(UserRole.ADMIN)
def project_index():
    """
    Function Name: project_index
    Description: Displays the project index page.
    """
    species = Species.query.order_by('common_name')
    return render_template('project/projects.html', species=species)

@project_bp.route('/list', methods=['GET', 'POST'])
def project_list():
    """
    Function Name: project_list
    Description: Retrieves a list of all projects.
    """
    # Logic to retrieve all projects
    projects = Project.query.join(Species).with_entities(
        Project.id,
        Project.name,
        Project.description,
        Species.common_name).order_by('name').all()
    print(projects)
    return jsonify({'projects':
                        [{
                            'id': prj.id,
                            'name': prj.name,
                            'description': prj.description,
                            'species': prj.common_name}
                         for prj in projects]})

# Add a new Project entry
@project_bp.route('/add', methods=['POST'])
@login_required
@role_required(UserRole.ADMIN)
def project_add():
    """
    Function Name: project_add
    Description: Adds a new project.
    """
    name = request.form.get('name')
    description = request.form.get('description')
    species_id = request.form.get('species_id')
    new_project = Project(name=name, description=description, species_id=species_id)
    db.session.add(new_project)
    db.session.commit()
    # Logic to save new_project to database
    return jsonify({'message': f'Project "{name}" added'}), 201

# Edit an existing Project entry
@project_bp.route('/edit/<int:project_id>', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.ADMIN)
def project_edit(project_id):
    """
    Function Name: project_edit
    Description: Edits an existing project.
    """
    project = Project.query.get(project_id)
    form = ProjectForm()

    newform = ProjectForm(data=form.data)
    newform.name.data = project.name
    newform.description.data = project.description
    newform.species_id.choices = [(species.id, species.common_name)
                               for species in Species.query.order_by('common_name')]
    newform.species_id.choices.insert(0, (0, 'Choose species'))
    newform.species_id.data = project.species_id

    error_response = form_submit_error_response(newform, 'project/project_edit.html')
    if error_response:
        return error_response

    if project.name != form.name.data:
        project.name = form.name.data
    if project.description != form.description.data:
        project.description = form.description.data
    if project.species_id != form.species_id.data:
        project.species_id = form.species_id.data

    db.session.commit()
    species = Species.query.order_by('common_name')
    return render_template('project/projects.html', species=species)


# Delete a Project entry
@project_bp.route('/delete/<int:project_id>', methods=['GET', 'DELETE'])
@login_required
@role_required(UserRole.ADMIN)
def project_delete(project_id):
    """
    Function Name: project_delete
    Description: Deletes a project by ID.
    """
    # Logic to find project by id and delete it
    project = Project.query.get(project_id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': f'Project {project.name} deleted'})
