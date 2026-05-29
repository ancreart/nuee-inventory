from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_babel import Babel

db       = SQLAlchemy()
migrate  = Migrate()
mail     = Mail()
csrf     = CSRFProtect()
babel    = Babel()