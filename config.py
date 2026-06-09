import os
import urllib.parse
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configuración base común a todos los entornos."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)

    MAIL_SERVER         = 'smtp.gmail.com'
    MAIL_PORT           = 587
    MAIL_USE_TLS        = True
    MAIL_USE_SSL        = False
    MAIL_DEBUG          = True
    MAIL_USERNAME       = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD       = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')

    LANGUAGES                = ['es', 'en', 'fr', 'pt']
    BABEL_DEFAULT_LOCALE     = 'es'
    BABEL_DEFAULT_TIMEZONE   = 'America/Bogota'


class DevelopmentConfig(Config):
    """Configuración para desarrollo."""
    DEBUG = True
    params = urllib.parse.quote_plus(
        "DRIVER=ODBC Driver 17 for SQL Server;"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=NueeDB;"
        "Trusted_Connection=yes;"
    )
    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"


class ProductionConfig(Config):
    """Configuración para producción."""
    DEBUG = False
    params = urllib.parse.quote_plus(
        "DRIVER=ODBC Driver 17 for SQL Server;"
        "SERVER=localhost;"
        "DATABASE=NueeProduccion;"
        "Trusted_Connection=yes;"
    )
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"mssql+pyodbc:///?odbc_connect={params}"
    )