"""
Module Name: data
Description: This module contains the data models for the application.
"""

import datetime
from enum import Enum

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class UserRole(Enum):
    """
    Class Name: UserRole
    Description: Enumeration of user roles.
    """
    SUPERUSER = 0
    ADMIN = 2
    MEMBER = 5
    GUEST = 9

class Role(db.Model):
    """
    Class Name: Role
    Description: Represents user roles in the application.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    level = db.Column(db.Integer, unique=True)
    # Permissions: manage_users, review_data, delete_records, etc.

class User(UserMixin, db.Model):
    """
    Class Name: User
    Description: Represents a user of the application.
    """
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, username, email, password, role_id, is_active=True, name=None):
        self.username = username
        self.email = email
        self.set_password(password)
        self.name = name
        self.role_id = role_id if role_id > 0 else 9
        self.is_active = is_active

    def set_password(self, password):
        """ Create hashed password. """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """ Compare given password to hashed user entry. """
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        """Only allow True response if the user is active."""
        return self.is_active

    # Optional: Implement __repr__ for easier debugging
    def __repr__(self):
        return f'<User {self.username}>'

class Project(db.Model):
    """
    Class Name: Project
    Description: Represents a project in the application.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(100), unique=True)
    sites = db.relationship('ProjectSite', backref='project')
    species_id = db.Column(db.Integer, db.ForeignKey('species.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))

    def __init__(self, name, description, species_id):
        self.name = name
        self.description = description
        self.species_id = species_id
        self.is_active = True

    def __repr__(self):
        return f'<Name {self.name}>'

class Site(db.Model):
    """
    Class Name: Site
    Description: Represents a site in the application.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(100), unique=True)
    points = db.relationship('Geography', backref='site')
    surveys = db.relationship('Survey', backref='site')
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f'<Name {self.name}>'

class ProjectSite(db.Model):
    """
    Class Name: ProjectSite
    Description: Represents a project site association.
    """
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))

    def __init__(self, project_id, site_id):
        self.project_id = project_id
        self.site_id = site_id

class Survey(db.Model):
    """
    Class Name: Survey
    Description: Represents a survey conducted at a site.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'))
    survey_date = db.Column(db.Date, nullable=False)
    time_start = db.Column(db.Time)
    time_end = db.Column(db.Time)
    observer_count = db.Column(db.Integer)
    comments = db.Column(db.Text)
    observations = db.relationship('Observation', backref='survey')
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))

    def __init__(self, user_id:int, project_id:int, site_id:int,
                 survey_date:str, time_start, time_end, observer_count, comments):
        self.user_id = user_id
        self.project_id = project_id
        self.site_id = site_id
        dsurvey = datetime.datetime.strptime(survey_date, '%Y-%m-%d').date()
        self.survey_date = dsurvey
        tstart = datetime.datetime.strptime(time_start, '%H:%M').time()
        tend = datetime.datetime.strptime(time_end, '%H:%M').time()
        self.time_start = tstart
        self.time_end = tend
        self.observer_count = observer_count
        self.comments = comments
    def __repr__(self):
        return (f'Survey <Project {self.project_id}, Site {self.site_id}, '
                f'Date {self.survey_date}, User {self.user_id}, '
                f'observer count {self.observer_count}>')

class Observation(db.Model):
    """
    Class Name: Observation
    Description: Represents an observation made during a survey.
    """
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'))
    species_id = db.Column(db.Integer, db.ForeignKey('species.id'))
    count = db.Column(db.Integer)
    count_supplemental = db.Column(db.Integer)
    latitude = db.Column(db.Float, nullable=True) # Optional: place where obs was made
    longitude = db.Column(db.Float, nullable=True) # Optional: place where obs was made
    direction = db.Column(db.String(5))
    behavior = db.Column(db.String(50))
    comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))

class Species(db.Model):
    """
    Class Name: Species
    Description: Represents a species in the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    species_code = db.Column(db.String(10), unique=True, index=True, nullable=False)
    common_name = db.Column(db.String(100), unique=True, nullable=False)
    scientific_name = db.Column(db.String(100), unique=True)
    rarity = db.Column(db.Integer, default=2) # 0=rare, 1=uncommon, 2=common
    status = db.Column(db.Boolean, default=True) # True=active, False=not in use
    comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))

    def __init__(self, species_code, common_name, scientific_name, rarity:int, status:bool):
        self.species_code =  species_code
        self.common_name = common_name
        self.scientific_name = scientific_name
        self.rarity = rarity
        self.common_name = common_name
        self.status = status

    def __repr__(self):
        return f'<Name {self.common_name} Code {self.species_code}>'

class Geography(db.Model):
    """
    Class Name: Geography
    Description: Represents geographical data associated with sites.
    """
    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'))
    geodetic_system = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    northing = db.Column(db.Float)
    easting = db.Column(db.Float)
    zone = db.Column(db.Integer)
    band = db.Column(db.String(1))

    def __init__(self, site_id, geodetic_system:str, latitude:float|None, longitude:float|None,
                 northing:float|None=None, easting:float|None=None, zone=None, band=None,
                 status:bool=True, comments=None):
        """

        :param site_id:             Site this point is for
        :param geodetic_system:     Typically UTM NAD83 or WGS84
        :param latitude:
        :param longitude:
        :param northing:            UTM northing
        :param easting:             UTM easting
        :param zone:                UTM vertical zone
        :param band:                UTM horizontal band
        :param status:              True=active, False=no longer in use
        :param comments:
        """

        if (latitude and longitude) or (northing and easting):
            self.site_id = site_id
            self.geodetic_system = geodetic_system
            self.latitude = latitude
            self.longitude = longitude
            self.northing = northing
            self.easting = easting
            self.zone = zone
            self.band = band
            self.status = status
            self.comments = comments


    def __repr__(self):
        return (f'<Site {self.site_id} '
                f'UTM ({self.northing}, {self.easting}) '
                f'WGS84 ({self.latitude}, {self.longitude})>')
