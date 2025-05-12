import unittest
from routes.ajax import url_get
class UtilsTests(unittest.TestCase):

    def test_get_url(self):
        # Example usage with a valid JSON API endpoint.
        lat, lon, wdate = 51.5074, -0.1278, "2023-06-01"
        # valid_url = "https://jsonplaceholder.typicode.com/todos/1"  # A reliable test URL
        invalid_url = "https://nonexistent-domain.example"
        non_json_url = "https://www.google.com"  # URL that returns HTML, not JSON
        openmeteo_url = f"https://archive-api.open-meteo.com/v1/archive" \
                        f"?latitude={lat}&longitude={lon}" \
                        f"&start_date={wdate}&end_date={wdate}" \
                        "&hourly=temperature_2m,weather_code," \
                        "rain,apparent_temperature,wind_speed_10m," \
                        "cloud_cover,cloud_cover_low,cloud_cover_mid," \
                        "surface_pressure,wind_direction_10m"

        url_get(openmeteo_url, True)
        url_get(invalid_url, False)
        url_get(non_json_url, False)
