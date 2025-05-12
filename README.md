# Flask App Overview

This Flask application serves as a comprehensive web solution that integrates various functionalities, including user authentication, data management, and reporting. It is designed to be modular and scalable, making it suitable for various use cases.

This Flask app is designed to be user-friendly and efficient, with a clear structure for easy navigation and maintenance. Feel free to explore the code and modify it according to your needs.

## Project Structure

```
Transerv/
         ├── app.py # Main application file 
         ├── cli.py # Command line interface commands
         ├── config.py # Configuration settings 
         ├── requirements.txt # Python package dependencies 
         ├── forms/ # Form definitions 
         ├── handlers/ # Request and error handlers 
         ├── models/ # Database models 
         ├── routes/ # Application routes 
         ├── static/ # Static files (CSS, JS, images) 
         ├── templates/ # HTML templates 
         ├── tests/ # Unit tests 
         └── user/ # User-related functionalities
```
## Usage

### Install Dependencies
   Ensure you have Python installed, then install the required packages using:
```bash
   pip install -r requirements.txt
 ```
   
### Configuration
The application can be configured through the _config.py_ file and the .env file.
The Config class in config.py allows you to manage database URIs and other settings.

#### .env
   Create a .env file with the necessary environment variables.
```
DB_USER=<your_database_user>
DB_PASS=<your_database_password>
DB_HOST=<your_database_host>
DB_PORT=<your_database_port>
DB_NAME=<your_database_name>
SQLITE_DB_FILE=<your_sqlite_db_file>
SECRET_KEY=<your_secret_key>
```

#### Sqlalchemy

`flask_sqlalchemy` requires the database URI to be set before initializing the database.
This application is pre-configured to use **SQLite** for development. You can 
use PostgreSQL in the production environment by setting the 
constant `SQLALCHEMY_DATABASE_URI` in ``config.py`` to use a PostgreSQL URI.

### Testing

Use **pytest** to run unit tests:
```bash
   pytest <source-directory>
```

### Run the application

#### Development
For development, debugging and testing functionality,  start the Flask development server:

```bash
   flask run
```

#### Production
For live production, install, configure and launch a **WSGI** server to run the Flask application.

**gunicorn**: Can use the sample configuration file provided `gunicorn --config gunicorn.py app:app`

**Docker**: 
The application can be run in a container using the sample `Dockerfile` and scripts
(`docker-build` and `docker-run`). These samples use the same port as the `gunicorn.py`

These are just examples and should be modified to suit your needs before trying them.