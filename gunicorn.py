"""
gunicorn configuration file
"""

import os

workers = int(os.environ.get('GUNICORN_PROCESSES', '2'))
threads = int(os.environ.get('GUNICORN_THREADS', '3'))

timeout = int(os.environ.get('GUNICORN_TIMEOUT', '60'))
bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8080')

forwarded_allow_ips = '*'  # Can be comma separated
secure_scheme_headers = { 'X-Forwarded-Proto': 'https' }
