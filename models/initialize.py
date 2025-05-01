import click
import os

from models.data import User, Role, UserRole, Location, Site, Geography, Species, Direction, Project

# Lookup data
compass_directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

# Sample data if you just want to test the database
sample_locations = [
    {'name': 'Upper', 'description': 'High land'},
    {'name': 'Lower', 'description': 'Low area'},
]

sample_sites = [
    {'location': 'Upper', 'name': 'Land1', 'description': 'On land'},
    {'location': 'Upper', 'name': 'Lake2', 'description': 'In Water'},
    {'location': 'Upper', 'name': 'Air3', 'description': 'Up in atmosphere'},
    {'location': 'Lower', 'name': 'Island4', 'description': 'island'},
    {'location': 'Lower', 'name': 'River5', 'description': 'Long waterway'},
]

sample_coords = [
    {'site': 'Land1', 'lat': 45.030841, 'lng': -74.674427},
    {'site': 'Lake2', 'lat': 45.019838, 'lng': -74.802194},
    {'site': 'Air3', 'lat': 44.983328, 'lng': -74.629196},
    {'site': 'Island4', 'lat': 45.014422, 'lng': -74.645509},
    {'site': 'River5', 'lat': 45.033821, 'lng': -74.577799}
]

sample_species = [
    {'code': 'CHICK', 'common_name': 'Chicken', 'scientific_name': 'Gallus Gallus'},
    {'code': 'GORIL', 'common_name': 'Gorilla', 'scientific_name': 'Gorilla Gorilla'},
    {'code': 'MOOSE', 'common_name': 'Moose', 'scientific_name': 'Alces Alces'},
    {'code': 'REDFOX', 'common_name': 'Red Fox', 'scientific_name': 'Vulpes Vulpes'},
]
def init_db_tables(app, db):
    with app.app_context():
        if db.session.query(Role).count() > 0:
            click.echo('FAILED: Database tables already exist.')
            return
        click.echo('Initializing database tables...')
        for role in UserRole:
            role = Role(name=role.name, level=role.value)
            db.session.add(role)
        db.session.commit()
        click.echo('Roles loaded successfully.')

        # Query for the 'id' column specifically
        role_id = db.session.query(Role.id). \
            filter(Role.level == 0).scalar()
        default_password = os.getenv('SUPER_PASSWORD', '7-survey-8')
        user = User(
            username='super',
            password=default_password,
            email='donotuse@super.com',
            role_id=role_id,
            status='active'
        )
        db.session.add(user)
        db.session.commit()
        click.echo('Super user loaded successfully.')

def load_lookups(app, db):
    with app.app_context():
        if Direction.query.first():
            click.echo('Lookup FAILED: tables already exist.')
            return
        click.echo('Initializing Lookup tables...')
        directions_to_add = []
        for direction in compass_directions:
            directions_to_add.append(Direction(code=direction)                                      )
        db.session.add_all(directions_to_add)
        db.session.commit()
        click.echo('Directions loaded successfully.')
def load_sites(app, db):

    locs_to_add = []
    sites_to_add = []
    geos_to_add = []
    if Location.query.first():
        click.echo('Database already contains locations. Skipping data loading.')
        return

    click.echo(f'Loading {len(sample_locations)} locations...')
    for data in sample_locations:
        loc = Location(name=data['name'], description=data['description'])
        locs_to_add.append(loc)
    for data in sample_sites:
        site = Site(loc_name=data['location'], name=data['name'], description=data['description'])
        sites_to_add.append(site)
    for data in sample_coords:
        # site_name, geodetic_system, latitude:float, longitude:float, northing:float, easting:
        geo = Geography(site_name=data['site'], geodetic_system='WGS84', latitude=data['lat'], longitude=data['lng'], northing=None, easting=None)
        geos_to_add.append(geo)
    with app.app_context():
        try:
            db.session.add_all(locs_to_add)
            db.session.add_all(sites_to_add)
            db.session.add_all(geos_to_add)
            db.session.commit()
            click.echo('Location loaded successfully.')
        except Exception as e:
            db.session.rollback()
            click.echo(f'Error loading data: {e}', err=True)

def load_species(app, db):

    species_to_add = []
    if Species.query.first():
        click.echo('Database already contains species. Skipping data loading.')
        return

    click.echo(f'Loading {len(sample_species)} species...')
    for data in sample_species:
        sp = Species(species_code=data['code'], common_name=data['common_name'], scientific_name=data['scientific_name'], rarity=2, status=True)
        species_to_add.append(sp)

    with app.app_context():
        try:
            db.session.add_all(species_to_add)
            db.session.commit()
            click.echo('Species data loaded successfully.')
        except Exception as e:
            db.session.rollback()
            click.echo(f'Error loading data: {e}', err=True)

def load_projects(app, db):

    if Project.query.first():
        click.echo('Database already contains projects. Skipping data loading.')
        return

    click.echo(f'Loading Projects...')
    projects_to_add = []
    projects_to_add.append(Project(name='Chicken', description='Countin chickens', species_code='CHICK'))

    with app.app_context():
        try:
            db.session.add_all(projects_to_add)
            db.session.commit()
            click.echo('projects data loaded successfully.')
        except Exception as e:
            db.session.rollback()
            click.echo(f'Error loading data: {e}', err=True)
