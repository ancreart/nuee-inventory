from app.extensions import db
from datetime import datetime

class ClienteProveedor(db.Model):
    __tablename__ = 'clienteproveedor'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nit = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(150), nullable=False)
    direccion = db.Column(db.String(150), nullable=False)
    celular = db.Column(db.String(20), nullable=False)
    tipo = db.Column(db.String(15), nullable=False)                          # Cliente / Proveedor
    tipo_identificacion = db.Column(db.String(5), nullable=True, default='NIT')  # CC, CE, NIT ← nuevo
    correo = db.Column(db.String(120), nullable=True)                        # ← nuevo

    def __repr__(self):
        return f"<ClienteProveedor {self.nombre}>"