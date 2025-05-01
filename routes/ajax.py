from flask import Blueprint, jsonify
from flask_login import login_required
from decorators import role_required
from models.data import db, Site, ProjectSite, UserRole, Geography

ajax_bp = Blueprint('ajax', __name__, url_prefix='/ajax')

@ajax_bp.route('/get_loc_sites/<int:location_id>')
def get_loc_sites(location_id):
    sites = Site.query.filter_by(location_id=location_id).all()
    data = [{'id': site.id, 'name': site.name, 'description': site.description, 'points': [{'lat':pt.latitude, 'lng':pt.longitude} for pt in site.points]} for site in sites]
    return jsonify(data)

@ajax_bp.route('/get_proj_sites/<int:project_id>')
def get_proj_sites(project_id):
    sites = ProjectSite.query.filter_by(project_id=project_id).join(Site).with_entities(ProjectSite.id, Site.name, Site.description).all()
    data = []
    for site in sites:
        points = Geography.query.filter_by(site_id=site.id).with_entities(Geography.latitude, Geography.longitude).all()
        data.append({'id': site.id, 'name': site.name, 'description': site.description, 'points': [{'lat':pt.latitude, 'lng':pt.longitude} for pt in points]})
    return jsonify(data)

@ajax_bp.route('/export')
@login_required
@role_required(UserRole.MEMBER)
def export_report(sql, fmt):
    if fmt not in ['csv', 'json']:
        return jsonify({'error': 'Invalid format type. Use "csv" or "json"'}), 400
    return jsonify({'data': db.engine.execute(sql).fetchall()}), 200

@ajax_bp.route('/get_weather/<int:location_id>')
def get_weather(lat, lon, wdate):
    OPEN_METEO_URL = f"https://archive-api.open-meteo.com/v1/archive"\
                      f"?latitude={lat}&longitude={lon}&start_date={wdate}&end_date={wdate}"\
                      "&hourly=temperature_2m,weather_code,rain,apparent_temperature,wind_speed_10m,"\
                      "cloud_cover,cloud_cover_low,cloud_cover_mid,surface_pressure,wind_direction_10m"

    sample_output = """{
  "latitude": 33.427063,
  "longitude": -112.02719,
  "generationtime_ms": 0.17249584197998,
  "utc_offset_seconds": 0,
  "timezone": "GMT",
  "timezone_abbreviation": "GMT",
  "elevation": 333,
  "hourly_units": {
    "time": "iso8601",
    "temperature_2m": "°C",
    "weather_code": "wmo code",
    "rain": "mm",
    "apparent_temperature": "°C",
    "wind_speed_10m": "km/h",
    "cloud_cover": "%",
    "cloud_cover_low": "%",
    "cloud_cover_mid": "%",
    "surface_pressure": "hPa",
    "wind_direction_10m": "°"
  },
  "hourly": {
    "time": [
      "2020-01-01T00:00",      "2020-01-01T01:00",      "2020-01-01T02:00",      "2020-01-01T03:00",      "2020-01-01T04:00",
      "2020-01-01T05:00",      "2020-01-01T06:00",      "2020-01-01T07:00",      "2020-01-01T08:00",      "2020-01-01T09:00",
      "2020-01-01T10:00",      "2020-01-01T11:00",      "2020-01-01T12:00",      "2020-01-01T13:00",      "2020-01-01T14:00",
      "2020-01-01T15:00",      "2020-01-01T16:00",      "2020-01-01T17:00",      "2020-01-01T18:00",      "2020-01-01T19:00",
      "2020-01-01T20:00",      "2020-01-01T21:00",      "2020-01-01T22:00",      "2020-01-01T23:00"
    ],
    "temperature_2m": [12.4, 9.7, 8.2, 7.8, 6.6, 5.9, 6.3, 7.4, 6.7, 4.8, 4.8, 4.2, 3.8, 3.1, 3.3, 2.9, 5.4, 7.4, 9.5, 11.3, 12.5, 13.3, 14, 14.2],
    "weather_code": [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 3, 3],
    "rain": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "apparent_temperature": [10.5, 7.4, 6.2, 5.7, 4.1, 3.4, 4.1, 5.9, 4.5, 1.6, 1, 0.5, 0, -0.3, -0.4, 0, 2.1, 4.3, 6.9, 8.8, 11, 11.7, 12.1, 11.9],
    "wind_speed_10m": [3.5, 8.2, 5.9, 5.5, 8.5, 7.8, 5.2, 0.4, 4.3, 10.3, 12.2, 11, 12.2, 9, 10.9, 5.9, 8.9, 8.9, 6.5, 7.1, 0.8, 1.5, 3.7, 6.5],
    "cloud_cover": [28, 38, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 6, 0, 0, 0, 28, 0, 0, 81, 82],
    "cloud_cover_low": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "cloud_cover_mid": [90, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "surface_pressure": [976.5, 976.7, 976.9, 976.9, 977, 977.2, 977.5, 977.9, 978.1, 977.8, 977.8, 977.8, 977, 978, 978.4, 978.9, 979.2, 979.5, 979.4, 977.7, 976.4, 974.6, 973.7, 973.8],
    "wind_direction_10m": [246, 293, 313, 23, 36, 13, 25, 90, 156, 115, 109, 101, 109, 95, 117, 101, 104, 111, 124, 135, 153, 166, 169, 304]
  }
} """