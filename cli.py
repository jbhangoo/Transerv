"""
CLI Commands
Register CLI commands to initialize the database
"""
import click
from models.data import db, User
from models.initialize import init_db_tables, load_sites, load_species, load_projects
# commands.py

def register_cli_commands(app):
    """
    # --- CLI Commands ---
    # These are flask command line utilities that run outside of the app
    # These are only to be executed when first generating the database
    # You may add your own utilities to customize the database table contents
    :param app: The flask app
    :return:
    """
    @app.cli.command("hello")
    def hello():
        """Say hello to NAME."""
        click.echo(f"context={app.name} . Database has {db.session.query(User).count()} users.")

    @app.cli.command("init_db")
    def init_db():
        """
            Creates the database tables.
            ONLY TO BE DONE ONCE AND FROM THE COMMAND LINE.
            1. Open Terminal (Bash, PowerShell, etc.)
            2. Navigate to this directory
            3. Run
                $ flask init_db
        :return:
        """
        db.create_all()
        print('Initialized the database.')
        init_db_tables(app, db)

    @app.cli.command("load_db")
    def load_db():
        """
            Loads the database tables with initial default test data.
            ONLY TO BE DONE ONCE AND FROM THE COMMAND LINE.
            1. Open Terminal (Bash, PowerShell, etc.)
            2. Navigate to this directory
            3. Run
                $ flask load_db
        :return:
        """
        load_sites(app, db)
        load_species(app, db)
        load_projects(app, db)
