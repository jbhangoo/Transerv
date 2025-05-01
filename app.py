from config import Config
from datetime import datetime
import os
from cli import register_cli_commands
from error_handlers import register_error_handlers
from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

from routes.ajax import ajax_bp
from routes.auth import auth_bp
from routes.reports import report_bp
from routes.user import user_bp
from routes.entry import entry_bp
from routes.projects import project_bp
from routes.projectsites import projectsite_bp
from models.data import db, User

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Config)
db.init_app(app)
csrf = CSRFProtect(app)  # Enables CSRF protection for all views

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in first.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

# Register Command Line Interfaces
register_cli_commands(app)

# Register error handlers
register_error_handlers(app)

# Register Routes and Blueprints
@app.route('/')
def index():  # put application's code here
    return render_template('dashboard.html')

app.register_blueprint(ajax_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(report_bp)
app.register_blueprint(entry_bp)
app.register_blueprint(project_bp)
app.register_blueprint(projectsite_bp)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(host=os.getenv('HOST', '0.0.0.0'), port=os.getenv('PORT', 5000), debug=os.getenv('DEBUG', True))
