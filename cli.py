import click
from models.data import db, User
from models.initialize import init_db_tables, load_sites, load_species, load_projects, load_lookups
# commands.py

def register_cli_commands(app):
    @app.cli.command("hello")
    def hello():
        """Say hello to NAME."""
        click.echo(f" You are in the {app.name} context. Database has {db.session.query(User).count()} users.")


    # --- CLI Commands ---
    # These are sample flask command line utilities that run outside of the app
    # These are only to be executed when first generating the database
    # You may add your own utilities to initialize the database table contents

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
            Loads the database tables with initial default data.
            ONLY TO BE DONE ONCE AND FROM THE COMMAND LINE.
            1. Open Terminal (Bash, PowerShell, etc.)
            2. Navigate to this directory
            3. Run
                $ flask load_db
        :return:
        """

        load_lookups(app, db)
        load_sites(app, db)
        load_species(app, db)
        load_projects(app, db)