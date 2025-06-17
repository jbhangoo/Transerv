""" errors.py -- error handlers """
from flask import render_template

def register_error_handlers(app):
    """
    Executing this method registers the error handlers for the given application
    :param app: register error handlers for this app
    :return:
    """

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('error/error.html',
                               error = f"Error 404 - Page not found ({error}"), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template('error/error.html',
                               error = f"Error 500 - Server error ({error}"), 500
