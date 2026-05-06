from app.extensions import db
from datetime import datetime


class Lote(db.Model):
    __tablename__ = 'lotes'

    id               = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_insumo        = db.Column(db.Integer, db.ForeignKey('insumos.id'), nullable=False)
    id_proveedor     = db.Column(db.Integer, nullable=True)
    numero_lote      = db.Column(db.String(20), nullable=False)
    cantidad         = db.Column(db.Integer, nullable=False, default=0)
    costo_compra     = db.Column(db.Numeric(10, 2), nullable=True, default=0)
    fecha_vencimiento= db.Column(db.Date, nullable=True)
    fecha_entrada    = db.Column(db.DateTime, default=datetime.utcnow)
    activo           = db.Column(db.Boolean, default=True)
    fecha_creacion   = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con insumo
    insumo = db.relationship('Insumo', backref='lotes')

    def __repr__(self):
        return f"<Lote {self.numero_lote} insumo={self.id_insumo}>"