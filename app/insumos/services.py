from app.extensions import db
from app.insumos.models import Insumo
from app.lotes.models import Lote
from flask import session


def crear_insumo(form):
    existe = Insumo.query.filter_by(codigo=form.codigo.data).first()
    if existe:
        raise ValueError("Ya existe un insumo con ese código")

    insumo = Insumo(
        codigo            = form.codigo.data,
        descripcion       = form.descripcion.data,
        lote              = form.lote.data,
        invima            = form.invima.data,
        valor             = form.valor.data,
        iva               = form.iva.data or 0,
        cantidad          = form.cantidad.data,
        stock_minimo      = form.stock_minimo.data,
        fecha_vencimiento = form.fecha_vencimiento.data,
        creado_por        = session.get('username', 'desconocido')
    )
    db.session.add(insumo)
    db.session.flush()

    if form.cantidad.data and form.cantidad.data > 0:
        from app.movimientos.models import Movimiento  # import local para evitar ciclo

        id_usuario     = session.get("id")
        nombre_usuario = session.get("nombre") or session.get("username") or "Desconocido"

        movimiento = Movimiento(
            id_cliente        = 1,
            id_insumo         = insumo.id,
            id_usuario        = id_usuario,
            nombre_usuario    = nombre_usuario,
            tipo              = "entrada",
            precio            = float(form.valor.data),
            cantidad          = form.cantidad.data,
            observaciones     = "Entrada inicial al crear insumo",
            fecha_vencimiento = form.fecha_vencimiento.data or None
        )
        db.session.add(movimiento)

    db.session.commit()
    return insumo


def actualizar_insumo(insumo_id, form):
    insumo = Insumo.query.get_or_404(insumo_id)
    insumo.codigo            = form.codigo.data
    insumo.descripcion       = form.descripcion.data
    insumo.lote              = form.lote.data
    insumo.invima            = form.invima.data
    insumo.valor             = form.valor.data
    insumo.iva               = form.iva.data or 0
    insumo.cantidad          = form.cantidad.data
    insumo.stock_minimo      = form.stock_minimo.data
    insumo.fecha_vencimiento = form.fecha_vencimiento.data
    insumo.activo            = form.activo.data if hasattr(form, 'activo') else insumo.activo
    db.session.commit()
    return insumo


def inactivar_insumo(insumo_id):
    insumo = Insumo.query.get_or_404(insumo_id)
    insumo.activo = False
    db.session.commit()


def eliminar_insumo(insumo_id):
    insumo = Insumo.query.get_or_404(insumo_id)
    Lote.query.filter_by(id_insumo=insumo_id).delete()
    db.session.delete(insumo)
    db.session.commit()


def listar_insumos_activos():
    return Insumo.query.filter_by(activo=True).all()


def listar_todos_insumos():
    return Insumo.query.order_by(Insumo.descripcion).all()


def obtener_insumo(insumo_id):
    return Insumo.query.get_or_404(insumo_id)


def buscar_insumos(query):
    if not query:
        return []
    busqueda = f"%{query}%"
    return Insumo.query.filter(
        db.or_(
            Insumo.descripcion.ilike(busqueda),
            Insumo.codigo.ilike(busqueda)
        ),
        Insumo.activo == True
    ).limit(10).all()


def obtener_insumo_por_codigo(codigo):
    return Insumo.query.filter_by(codigo=codigo, activo=True).first()