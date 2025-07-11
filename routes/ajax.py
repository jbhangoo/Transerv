"""
Module Name: ajax
Description: This module contains AJAX routes for handling asynchronous requests.
"""
import json
import requests

from flask import Blueprint, jsonify
from flask_login import login_required
from sqlalchemy.orm import joinedload

from handlers.decorators import role_required
from models.data import db, Site, ProjectSite, UserRole

ajax_bp = Blueprint('ajax', __name__, url_prefix='/ajax')

@ajax_bp.route('/get_proj_sites/<int:project_id>')
def get_proj_sites(project_id):
    """
    Returns a JSON response containing site details and their geographical points.
    :param project_id:
    :return:
    """
    sites = (db.session.query(ProjectSite, Site)
             .join(Site, ProjectSite.site_id == Site.id)
             .filter(ProjectSite.project_id == project_id)
             .options(joinedload(Site.points))
             .all())

    data = []
    for project_site, site in sites:
        points = [{'id': p.id, 'lat': p.latitude, 'lng': p.longitude}
                  for p in site.points]
        data.append({
            'id': project_site.id,
            'site_id': site.id,
            'name': site.name,
            'description': site.description,
            'points': points
        })
    print("get_proj_sites",data)
    return jsonify(data)

@ajax_bp.route('/export')
@login_required
@role_required(UserRole.MEMBER)
def export_report(sql, fmt):
    """
    Description: Exports a report based on the provided SQL query and format.
    Returns a JSON response containing the exported data.
    :param sql:
    :param fmt:
    :return:
    """
    if fmt not in ['csv', 'json']:
        return jsonify({'error': 'Invalid format type. Use "csv" or "json"'}), 400
    return jsonify({'files': db.engine.execute(sql).fetchall()}), 200

@ajax_bp.route('/get_weather/<int:site_id>')
def get_weather(site_id:int):
    """
    Get weather. See open-meteo.com for details. Example output format at end of this file.
    :param site_id:
    :return:
    """
    site = Site.query.filter_by(site_id=site_id).first()
    lat, lon, wdate = site.lat
    openmeteo_url = f"https://archive-api.open-meteo.com/v1/archive"\
                    f"?latitude={lat}&longitude={lon}"\
                    f"&start_date={wdate}&end_date={wdate}"\
                     "&hourly=temperature_2m,weather_code,"\
                     "rain,apparent_temperature,wind_speed_10m,"\
                     "cloud_cover,cloud_cover_low,cloud_cover_mid,"\
                     "surface_pressure,wind_direction_10m"
    weather_data = get_json_from_url(openmeteo_url)
    if weather_data:
        print("Successfully retrieved JSON files:")
        print(json.dumps(weather_data, indent=2))  # Use json.dumps for pretty printing

        # Accessing files within the JSON object (assuming it's a dictionary)
        print(f"Title: {weather_data.get('title')}")
        print(f"Completed: {weather_data.get('completed')}")
    else:
        print("Failed to retrieve JSON files from open-meteo.com")

def get_json_from_url(url):
    """
    Sends a GET request to the specified URL and converts the JSON response
    into a Python object (usually a dictionary or a list).  Handles common
    errors and returns None on failure.

    Args:
        url (str): The URL to send the GET request to.

    Returns:
        object:  A Python object representing the JSON files, or None if
                 the request or JSON decoding fails.
    """
    response = {'text':''}
    try:
        # Send a GET request to the URL.  We use a timeout to prevent
        # the program from hanging indefinitely on a slow or unresponsive server.
        response = requests.get(url, timeout=10)  # Timeout after 10 seconds

        # Raise an exception for bad status codes (4xx or 5xx).
        response.raise_for_status()

        # Parse the JSON response.  This will raise a json.JSONDecodeError
        # if the response is not valid JSON.
        json_data = response.json()
        return json_data

    except requests.exceptions.Timeout:
        return {"error": f"Request to {url} took too long to respond."}
    except requests.exceptions.TooManyRedirects:
        return {"error": f"Too many redirects. '{url}' might be misconfigured."}
    except requests.exceptions.RequestException as e:
        # Handle network errors (e.g., connection refused, timeout, invalid URL).
        # Handle network-related errors
        error_type = type(e).__name__
        return {"error": f"Network Error ({error_type})  with '{url}': {str(e)}"}

    except json.JSONDecodeError as e:
        # Handle errors in the JSON decoding process.  This usually means the
        # server returned a response that was not valid JSON.
        return {"error": f"Error decoding JSON response from {url}: {str(e)}"}

    except (ValueError, TypeError) as e:
        return {"error": f"Unexpected format. Error: {str(e)}"}
    except (KeyError, IndexError) as e:
        return {"error": f"Missing data. Error: {str(e)}"}
    except AttributeError as e:
        return {"error": f"Invalid operation. Maybe bad data. Error: {str(e)}"}
    except Exception as e:
        # Catch-all for any other unexpected exceptions
        error_type = type(e).__name__
        return {"error": f"Unexpected error ({error_type}) from {url}: {str(e)}"}


def url_get(url:str, expected_result:bool):
    """
    Useful for testing get_json_from_url with a URL
    :param url:                 GET json from this url
    :param expected_result:     Is this expected to succeed? For error testing
    :return:
    """
    data = get_json_from_url(url)
    if data:
        print(f"Successfully retrieved JSON files "
              f"({ 'expected' if expected_result else 'unexpected'}):")
        print(json.dumps(data, indent=2))  # Use json.dumps for pretty printing
    else:
        print(f"Failed to retrieve JSON files from {url}")

"""
Example output of weather data
{
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
        "2020-01-01T00:00",      "2020-01-01T01:00",      "2020-01-01T02:00",
        "2020-01-01T03:00",      "2020-01-01T04:00",      "2020-01-01T05:00",
        "2020-01-01T06:00",      "2020-01-01T07:00",      "2020-01-01T08:00",
        "2020-01-01T09:00",      "2020-01-01T10:00",      "2020-01-01T11:00",
        "2020-01-01T12:00",      "2020-01-01T13:00",      "2020-01-01T14:00",
        "2020-01-01T15:00",      "2020-01-01T16:00",      "2020-01-01T17:00",
        "2020-01-01T18:00",      "2020-01-01T19:00",      "2020-01-01T20:00",
        "2020-01-01T21:00",      "2020-01-01T22:00",      "2020-01-01T23:00"
    ],
    "temperature_2m": [12.4, 9.7, 8.2, 7.8, 6.6, 5.9, 6.3, 7.4, 6.7, 4.8,
     4.8, 4.2, 3.8, 3.1, 3.3, 2.9, 5.4, 7.4, 9.5, 11.3, 12.5, 13.3, 14, 14.2],
    "weather_code": [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 3, 3],
    "rain": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "apparent_temperature": [10.5, 7.4, 6.2, 5.7, 4.1, 3.4, 4.1, 5.9, 4.5, 1.6, 1, 0.5,
     0, -0.3, -0.4, 0, 2.1, 4.3, 6.9, 8.8, 11, 11.7, 12.1, 11.9],
    "wind_speed_10m": [3.5, 8.2, 5.9, 5.5, 8.5, 7.8, 5.2, 0.4, 4.3, 10.3, 12.2, 11, 12.2,
     9, 10.9, 5.9, 8.9, 8.9, 6.5, 7.1, 0.8, 1.5, 3.7, 6.5],
    "cloud_cover": [28, 38, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 6, 0, 0, 0, 28, 0, 0, 81, 82],
    "cloud_cover_low": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "cloud_cover_mid": [90, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "surface_pressure": [976.5, 976.7, 976.9, 976.9, 977, 977.2, 977.5, 977.9, 978.1, 977.8, 977.8,
     977.8, 977, 978, 978.4, 978.9, 979.2, 979.5, 979.4, 977.7, 976.4, 974.6, 973.7, 973.8],
    "wind_direction_10m": [246, 293, 313, 23, 36, 13, 25, 90, 156, 115, 109, 101, 109, 95, 117,
     101, 104, 111, 124, 135, 153, 166, 169, 304]
  }
}
"""
