"""
Module Name: initialize
Description: Functions that initialize the database and load with basic sample data
"""
import os
from sqlalchemy.exc import IntegrityError, OperationalError
from models.data import User, Role, UserRole, Site, Geography, Species, Project, ProjectSite

# Simple example data if you just want to test the app with basic actions
# Assumes the database is empty. Replace with your own data if needed
sample_sites = [
    {'name': 'Land1', 'description': 'On land'},
    {'name': 'Lake2', 'description': 'In Water'},
    {'name': 'Air3', 'description': 'Up in atmosphere'},
    {'name': 'Island4', 'description': 'island'},
    {'name': 'River5', 'description': 'Long waterway'},
]

sample_coords = [
    {'site_id': 1, 'lat': 45.030841, 'lng': -74.674427},
    {'site_id': 1, 'lat': 45.019838, 'lng': -74.802194},
    {'site_id': 1, 'lat': 45.014422, 'lng': -74.645509},
    {'site_id': 2, 'lat': 44.983328, 'lng': -74.629196},
    {'site_id': 2, 'lat': 45.033821, 'lng': -74.577799},
    {'site_id': 3, 'lat': 42.983328, 'lng': -76.629196},
    {'site_id': 3, 'lat': 42.135881, 'lng': -76.577799},
    {'site_id': 3, 'lat': 42.033821, 'lng': -76.577799}
]

sample_projectsites = [
    {'project_id': 1, 'site_id': 1},
    {'project_id': 1, 'site_id': 2},
    {'project_id': 2, 'site_id': 3},
    {'project_id': 1, 'site_id': 4},
    {'project_id': 2, 'site_id': 5},
]

sample_species = [
    {'code': 'CHICK', 'common_name': 'Chicken', 'scientific_name': 'Gallus Gallus'},
    {'code': 'GORILLA', 'common_name': 'Gorilla', 'scientific_name': 'Gorilla Gorilla'},
    {'code': 'MOOSE', 'common_name': 'Moose', 'scientific_name': 'Alces Alces'},
    {'code': 'REDFOX', 'common_name': 'Red Fox', 'scientific_name': 'Vulpes Vulpes'},
]
### End of Sample Data ###

def init_db_tables(app, db):
    """
    Set up the database
    :param app:
    :param db:
    :return:
    """
    with app.app_context():
        if db.session.query(Role).count() > 0:
            print('Database already contains roles. Skipping.')
            return
        print('Initializing database tables...')
        for role in UserRole:
            role = Role(name=role.name, level=role.value)
            db.session.add(role)
        db.session.commit()
        print('Roles loaded successfully.')

        # Query for the 'id' column specifically
        role_id = db.session.query(Role.id). \
            filter(Role.level == 0).scalar()
        default_password = os.getenv('SUPER_PASSWORD', '7-survey-8')
        user = User(
            username='super',
            password=default_password,
            email='donotuse@super.com',
            role_id=role_id,
            is_active=True,
        )
        db.session.add(user)
        db.session.commit()
        print('Super user loaded successfully.')

def load_sites(app, db):
    """
    Load basic set of sample data into a new database
    :param app:
    :param db:
    :return:
    """
    if Site.query.first():
        print('Database already contains sites. Skipping.')
        return

    print(f'Loading {len(sample_sites)} sites...')
    sites_to_add = []
    for data in sample_sites:
        site = Site(name=data['name'], description=data['description'])
        sites_to_add.append(site)

    print('Add points to sites...')
    geos_to_add = []
    for data in sample_coords:
        # site_name, geodetic_system, latitude:float, longitude:float, northing:float, easting:
        geo = Geography(site_id=data['site_id'], geodetic_system='WGS84',
                        latitude=data['lat'], longitude=data['lng'], northing=None, easting=None)
        geos_to_add.append(geo)

    print('Add projects to sites...')
    proj_sites_to_add = []
    for data in sample_projectsites:
        ps = ProjectSite(project_id=data['project_id'], site_id=data['site_id'])
        proj_sites_to_add.append(ps)

    with app.app_context():
        try:
            db.session.add_all(sites_to_add)
            db.session.commit()
            print('Sites loaded successfully.')
            db.session.add_all(geos_to_add)
            db.session.commit()
            print('Coords loaded successfully.')
            db.session.add_all(proj_sites_to_add)
            db.session.commit()
            print('Project sites loaded successfully.')
        except (IntegrityError, OperationalError) as e:
            db.session.rollback()
            print(f'Error loading files: {str(e)}')

def load_species(app, db):
    """

    :param app:
    :param db:
    :return:
    """
    species_to_add = []
    if Species.query.first():
        print('Database already contains species. Skipping files loading.')
        return

    print(f'Loading {len(sample_species)} species...')
    for data in sample_species:
        sp = Species(species_code=data['code'], common_name=data['common_name'],
                     scientific_name=data['scientific_name'], rarity=2, status=True)
        species_to_add.append(sp)

    with app.app_context():
        try:
            db.session.add_all(species_to_add)
            db.session.commit()
            print('Species files loaded successfully.')
        except (IntegrityError, OperationalError) as e:
            db.session.rollback()
            print(f'Error loading files: {e}')

def load_projects(app, db):
    """

    :param app:
    :param db:
    :return:
    """
    if Project.query.first():
        print('Database already contains projects. Skipping files loading.')
        return

    print('Loading Projects...')
    projects_to_add = []
    species_id = Species.query.filter_by(species_code='CHICK').first().id
    projects_to_add.append(Project(name='Chicken',
                                   description='Countin chickens',
                                   species_id=species_id))

    with app.app_context():
        try:
            db.session.add_all(projects_to_add)
            db.session.commit()
            print('projects files loaded successfully.')
        except (IntegrityError, OperationalError) as e:
            db.session.rollback()
            print(f'Error loading files: {str(e)}')
