# error_handlers.py
from flask import render_template

def register_error_handlers(app):

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('error/error.html',
                               error = f"Error 404 - Page not found ({error}"), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template('error/error.html',
                               error = f"Error 500 - Server error ({error}"), 500
