import os
import urllib.parse
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configuración base (común a todos los entornos)"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'woody2026')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_PERMANENT = False

    # Duración de la sesión cuando se marca "Recordar contraseña"
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)

    # Mail
    MAIL_SERVER         = 'smtp.gmail.com'
    MAIL_PORT           = 587
    MAIL_USE_TLS        = True
    MAIL_USE_SSL        = False
    MAIL_DEBUG          = True
    MAIL_USERNAME       = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD       = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')


class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True

    params = urllib.parse.quote_plus(
        "DRIVER=ODBC Driver 17 for SQL Server;"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=Farmacia2026;"
        "Trusted_Connection=yes;"
    )

    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"


class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False

    params = urllib.parse.quote_plus(
        "DRIVER=ODBC Driver 17 for SQL Server;"
        "SERVER=localhost;"
        "DATABASE=DatosFarmacia;"
        "Trusted_Connection=yes;"
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"mssql+pyodbc:///?odbc_connect={params}"
    )