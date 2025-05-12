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
    SQLALCHEMY_DATABASE_URI = SQLITE_SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-here')
