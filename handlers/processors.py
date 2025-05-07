from datetime import datetime

def register_request_processors(app):
    @app.before_request
    def before_callback():
        # Runs before each request
        return None

    @app.after_request
    def after_callback(response):
        # Runs after each request
        return response

    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}
