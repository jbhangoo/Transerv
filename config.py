"""
Configuration file for env variables
"""
import os
from dotenv import load_dotenv

load_dotenv()

SQLITE_SQLALCHEMY_DATABASE_URI = ("sqlite:///"
                                  + os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                 os.getenv('SQLITE_DB_FILE')))
POSTGRESQL_SQLALCHEMY_DATABASE_URI = (f"postgresql://{os.getenv('DB_USER')}:"
                                    f"{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:"
                                    f"{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
                                    f"?sslmode=require")

class Config:
    """
    Load required environment variables and database configuration
    """
    SQLALCHEMY_DATABASE_URI = SQLITE_SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-here')

    # Database connection pool settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,           # Number of connections to keep open in the pool
        'max_overflow': 20,        # Number of connections to allow in overflow
        'pool_timeout': 30,        # Seconds to wait before giving up on getting a connection
        'pool_recycle': 1800,      # Recycle connections after 30 minutes
        'pool_pre_ping': True      # Enable connection health checks
    }
