import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URI_sqlite = ("sqlite:///"
                                  + os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                 os.getenv('SQLITE_DB_FILE')))
SQLALCHEMY_DATABASE_URI_postgres = (f"postgresql://{os.getenv('DB_USER')}:"
                                    f"{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:"
                                    f"{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
                                    f"?sslmode=require")

class Config:
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI_sqlite
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-here')
