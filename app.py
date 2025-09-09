"""
Main application module for the entry point into the Flask application.

- creates the Flask application
- Sets CSRF protection
- Loads configuration
- configures the database
- Starts logging
- Sets up the login manager
. Registers the request processors, error handlers, CLI for database initialization
- Registers the route blueprints
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_required

from handlers.processors import register_request_processors
from handlers.errors import register_error_handlers

from cli import register_cli_commands
from config import Config
from routes.ajax import ajax_bp
from routes.auth import auth_bp
from routes.reports import report_bp
from routes.user import user_bp
from routes.entry import entry_bp
from routes.projects import project_bp
from routes.projectsites import projectsite_bp
from models.data import db, User

app = Flask(__name__, template_folder='templates', static_folder='static')
csrf = CSRFProtect(app)         # Enables CSRF protection for all views
app.config.from_object(Config)  # Read config from .env

# Initialize SQLAlchemy with engine options
db.init_app(app)

# Apply engine options from config
with app.app_context():
    # This ensures the engine options are used when the engine is created
    db.engine.dispose()  # Close any existing connections to apply new settings

# Set up logging
if not app.debug:  # Only set up logging if not in debug mode
    logfile_handler = RotatingFileHandler(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/files', 'wildlife.log'),
        maxBytes=10_000, backupCount=3)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    logfile_handler.setFormatter(formatter)
    logfile_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(logfile_handler)

app.logger.setLevel(logging.INFO)  # Set the logging level for the application logger itself
app.logger.info("Started")

# Use flask_login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in first.'

@login_manager.user_loader
def load_user(user_id):
    """
    Callback to reload the user object from the user ID stored in the session
    :param user_id:
    :return:
    """
    return User.query.get(int(user_id))

# Register request processors
register_request_processors(app)

# Register error handlers
register_error_handlers(app)

# Register Command Line Interfaces
register_cli_commands(app)

# Register Routes and Blueprints
@app.route('/')
@login_required
def index():
    """ Main dashboard page for the application """
    return render_template('dashboard.html')

app.register_blueprint(ajax_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(report_bp)
app.register_blueprint(entry_bp)
app.register_blueprint(project_bp)
app.register_blueprint(projectsite_bp)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(host=os.getenv('HOST', '0.0.0.0'),
            port=int(os.getenv('PORT', '5000')),
            debug=bool(os.getenv('DEBUG', 'True')))
