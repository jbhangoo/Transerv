""" processors.py - Register processor hooks """
from datetime import datetime
from flask import current_app, request

def register_request_processors(app):
    """ Executing this method registers processors that run before and/or after other actions. """

    @app.before_request
    def before_callback():
        """ What to run before each request """
        args_str = ', '.join(f'{key}={value}' for key, value in request.args.items())
        current_app.logger.info(f'{request.method} {request.url}: Start ({args_str})')

    @app.after_request
    def after_callback(response):
        """ What to run after each request """
        current_app.logger.info(f'{request.method} {request.url}: Ended {response.status}')
        return response

    @app.context_processor
    def inject_now():
        """ What to inject into each template context: definition of 'now' """
        return {'now': datetime.now()}
