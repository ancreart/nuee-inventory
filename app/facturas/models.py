from app.extensions import db
from datetime import datetime

class Factura(db.Model):
    __tablename__ = 'facturas'
    id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero        = db.Column(db.String(20), unique=True, nullable=False)
    id_cliente    = db.Column(db.Integer, nullable=False)
    fecha         = db.Column(db.DateTime, default=datetime.utcnow)
    subtotal      = db.Column(db.Numeric(10, 2), default=0)
    total_iva     = db.Column(db.Numeric(10, 2), default=0)
    total         = db.Column(db.Numeric(10, 2), default=0)
    estado        = db.Column(db.String(20), default='Pendiente')
    observaciones = db.Column(db.String(300), nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    nombre_usuario = db.Column(db.String(100), nullable=True)
    detalles = db.relationship('FacturaDetalle', backref='factura', lazy=True,
                               cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Factura {self.numero}>"


class FacturaDetalle(db.Model):
    __tablename__ = 'factura_detalles'
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_factura      = db.Column(db.Integer, db.ForeignKey('facturas.id'), nullable=False)
    id_insumo       = db.Column(db.Integer, nullable=False)
    descripcion     = db.Column(db.String(150), nullable=False)
    cantidad        = db.Column(db.Integer, nullable=False, default=1)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    iva             = db.Column(db.Numeric(5, 2), default=0)
    subtotal        = db.Column(db.Numeric(10, 2), default=0)

    def __repr__(self):
        return f"<FacturaDetalle factura={self.id_factura} insumo={self.id_insumo}>"