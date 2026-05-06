from app.extensions import db
from app.lotes.models import Lote


def crear_lote(data):
    lote = Lote(
        id_insumo=data.get('id_insumo'),
        id_proveedor=data.get('id_proveedor') or None,
        numero_lote=data.get('numero_lote'),
        cantidad=int(data.get('cantidad', 0)),
        costo_compra=data.get('costo_compra') or 0,
        fecha_vencimiento=data.get('fecha_vencimiento') or None,
        fecha_entrada=data.get('fecha_entrada') or None,
    )
    db.session.add(lote)
    db.session.commit()
    return lote


def listar_lotes_por_insumo(id_insumo):
    return Lote.query.filter_by(
        id_insumo=id_insumo, activo=True
    ).order_by(Lote.fecha_entrada.desc()).all()


def obtener_lote(lote_id):
    return Lote.query.get_or_404(lote_id)


def eliminar_lote(lote_id):
    lote = Lote.query.get_or_404(lote_id)
    lote.activo = False
    db.session.commit()