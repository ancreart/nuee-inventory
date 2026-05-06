from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nombre        = db.Column(db.String(100))
    email         = db.Column(db.String(120), unique=True, nullable=True)
    rol           = db.Column(db.String(20))
    activo        = db.Column(db.Boolean, default=True)

    # Recuperación de contraseña
    reset_token         = db.Column(db.String(100), nullable=True)
    reset_token_expiry  = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def token_valido(self):
        if not self.reset_token or not self.reset_token_expiry:
            return False
        return datetime.utcnow() < self.reset_token_expiry