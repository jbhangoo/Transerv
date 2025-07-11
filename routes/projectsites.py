"""
Module Name: projectsites
Description: This module contains routes related to projects and sites.
"""
import json
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required, current_user

from handlers.decorators import role_required, UserRole
from models.data import db, Project, Site, ProjectSite, Geography

projectsite_bp = Blueprint('projectsites', __name__, url_prefix='/projectsites')


@projectsite_bp.route('/', methods=['GET'])
@login_required
@role_required(UserRole.ADMIN)
def projectsite_index():
    """
    Function Name: projectsite_index
    Description: Displays the projectsites index page.
    :return:
    """
    projects = Project.query.all()
    sites = Site.query.all()
    return render_template('project/projectsites.html',
                           current_user=current_user,
                           projects=projects, sites=sites)

@projectsite_bp.route('/list', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.ADMIN)
def projectsite_list():
    """
    Function Name: projectsite_list
    Description: Displays all project sites
    :return:
    """

    projectsites = ProjectSite.query.join(Project).join(Site).with_entities(
        ProjectSite.id,
        Project.name.label('project'),
        Site.name.label('site'),
    ).all()
    return jsonify({'projectsites': [{'id': sp.id, 'project': sp.project, 'site': sp.site}
                                     for sp in projectsites]})

# Add a new ProjectSite entry
@projectsite_bp.route('/add', methods=['POST'])
@login_required
@role_required(UserRole.ADMIN)
def projectsite_add():
    """
    Function Name: projectsite_add
    Description: Adds a new project site
    :return:
    """
    project_id = request.form.get('project_id')
    site_name = request.form.get('siteName')
    description = request.form.get('siteDescription')

    # Extract points (which was added as a JSON string)
    points_json = request.form.get('points')
    points = json.loads(points_json) if points_json else []

    if not project_id:
        return jsonify({'message': 'Project ID is required'}), 400
    if not site_name:
        return jsonify({'message': 'Site name is required'}), 400
    new_site = Site(name=site_name, description=description)
    try:
        db.session.add(new_site)
        db.session.flush()  # Ensure new_site.id is available for use
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Database error: Does Site already exist?'}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Database error occurred: ' + str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

    db.session.flush()  # Ensure new_site.id is available for use

    # Add points to Geography table
    for point in points:
        new_geography = Geography(site_id=new_site.id, geodetic_system='WGS84',
                                 latitude=point['latitude'], longitude=point['longitude'])
        db.session.add(new_geography)
    db.session.commit()

    # Add ProjectSite
    site_id = Site.query.filter_by(name=site_name).first().id
    new_projectsite = ProjectSite(project_id=project_id, site_id=site_id)
    db.session.add(new_projectsite)
    db.session.commit()

    return jsonify({'message': 'ProjectSite added'}), 201

# Edit an existing ProjectSite entry
@projectsite_bp.route('/edit/<int:site_id>', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.ADMIN)
def projectsite_edit(site_id):
    """
    Function Name: projectsite_edit
    Description: Edits a site of a project
    :param site_id:
    :return:
    """
    site = Site.query.get(site_id)
    site_data = {
        'id': site.id,
        'name': site.name,
        'description': site.description,
        'points': [{'id': p.id, 'latitude': p.latitude, 'longitude': p.longitude}
                   for p in site.points]
    }
    if request.method == 'GET':
        return render_template('project/projectsite_edit.html',
                               site=site_data,
                               current_user=current_user)
    if request.method == 'POST':
        formdata = request.get_json()
        if ('name' in formdata) and (site.name != formdata['name']):
            site.name = formdata['name']
        if ('description' in formdata) and (site.description != formdata['description']):
            site.description = formdata['description']
        if ('points' in formdata) and (site.points != formdata['points']):
            # Clear existing points
            site.points.clear()

            # Add new points
            for point in formdata['points']:
                if 'latitude' in point and 'longitude' in point:
                    site.points.append(
                        Geography(
                            site_id=site.id,
                            geodetic_system='WGS84',
                            latitude=float(point['latitude']),
                            longitude=float(point['longitude']),
                            northing=None,
                            easting=None
                        )
                    )

        db.session.commit()

        # Return a JSON response
        return jsonify({
            'status': 'success',
            'message': 'Site updated successfully',
        }), 200

    return "Method not supported", 405 # Should never get here anyway

# Delete a ProjectSite entry
@projectsite_bp.route('/delete/<int:psid>', methods=['DELETE'])
@login_required
@role_required(UserRole.ADMIN)
def projectsite_delete(psid):
    """
    Function Name: projectsite_delete
    Description: Deletes a project site
    :param psid:
    :return:
    """
    projectsite = ProjectSite.query.get(psid)
    db.session.delete(projectsite)
    db.session.commit()
    return jsonify({'message': f'ProjectSite {projectsite.id} deleted'})
