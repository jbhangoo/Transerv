from datetime import datetime
from flask import current_app, request

def register_request_processors(app):
    @app.before_request
    def before_callback():
        # Runs before each request
        args_str = ', '.join(f'{key}={value}' for key, value in request.args.items())
        current_app.logger.info(f'{request.method} {request.url}: Start ({args_str})')

    @app.after_request
    def after_callback(response):
        # Runs after each request
        current_app.logger.info(f'{request.method} {request.url}: Ended {response.status}')
        return response

    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}
