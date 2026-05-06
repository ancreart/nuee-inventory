from app.extensions import db
from datetime import datetime


class Movimiento(db.Model):
    __tablename__ = "movimientos"

    id                = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente        = db.Column(db.Integer, nullable=False)
    id_insumo         = db.Column(db.Integer, nullable=False)
    id_usuario        = db.Column(db.Integer, nullable=True)
    nombre_usuario    = db.Column(db.String(100), nullable=True)
    tipo              = db.Column(db.String(20), nullable=False, default='salida')
    precio            = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    cantidad          = db.Column(db.Integer, nullable=False, default=0)
    fecha_creacion    = db.Column(db.DateTime, default=datetime.utcnow)
    observaciones     = db.Column(db.String(150), nullable=True)
    fecha_vencimiento = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"<Movimiento {self.id}>"