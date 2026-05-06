from app.extensions import db
from app.facturas.models import Factura, FacturaDetalle
from app.movimientos.models import Movimiento
from app.insumos.models import Insumo
from app.auth.models import Usuario
from flask import session
from datetime import datetime


def generar_numero_factura():
    ultima = Factura.query.order_by(Factura.id.desc()).first()
    if ultima:
        num = int(ultima.numero.split('-')[1]) + 1
    else:
        num = 1
    return f"FAC-{num:03d}"


def crear_factura(id_cliente, items, observaciones=''):
    """
    items: lista de dicts con keys:
      id_insumo, descripcion, cantidad, precio_unitario, iva
    """
    # Validar stock de todos los items ANTES de crear nada
    for item in items:
        insumo = Insumo.query.get(item['id_insumo'])
        if not insumo:
            raise ValueError(f"El producto con ID {item['id_insumo']} no existe")
        cant = int(item['cantidad'])
        if insumo.cantidad < cant:
            raise ValueError(
                f"Stock insuficiente para '{insumo.descripcion}'. "
                f"Disponible: {insumo.cantidad}, solicitado: {cant}"
            )

    numero    = generar_numero_factura()
    subtotal  = 0
    total_iva = 0

    nombre_usuario = session.get('nombre') or session.get('username') or 'Desconocido'

    factura = Factura(
        numero         = numero,
        id_cliente     = id_cliente,
        observaciones  = observaciones,
        estado         = 'Pendiente',
        nombre_usuario = nombre_usuario
    )
    db.session.add(factura)
    db.session.flush()

    for item in items:
        precio   = float(item['precio_unitario'])
        cant     = int(item['cantidad'])
        iva_pct  = float(item.get('iva', 0))
        sub_item = precio * cant
        iva_item = sub_item * (iva_pct / 100)
        subtotal  += sub_item
        total_iva += iva_item

        detalle = FacturaDetalle(
            id_factura      = factura.id,
            id_insumo       = item['id_insumo'],
            descripcion     = item['descripcion'],
            cantidad        = cant,
            precio_unitario = precio,
            iva             = iva_pct,
            subtotal        = sub_item + iva_item
        )
        db.session.add(detalle)

        # Descontar stock del insumo
        insumo           = Insumo.query.get(item['id_insumo'])
        insumo.cantidad -= cant

        # Movimiento de salida automático
        movimiento = Movimiento(
            id_cliente     = id_cliente,
            id_insumo      = item['id_insumo'],
            nombre_usuario = nombre_usuario,
            tipo           = 'salida',
            precio         = precio,
            cantidad       = cant,
            observaciones  = f"Factura {numero}",
            fecha_creacion = datetime.utcnow()
        )
        db.session.add(movimiento)

    factura.subtotal  = subtotal
    factura.total_iva = total_iva
    factura.total     = subtotal + total_iva

    db.session.commit()
    return factura