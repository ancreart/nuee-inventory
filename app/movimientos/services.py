from app.extensions import db
from app.movimientos.models import Movimiento
from app.insumos.models import Insumo
from app.clienteproveedor.models import ClienteProveedor
from app.auth.models import Usuario
from datetime import datetime
from flask import session
import random
import string


def obtener_o_crear_usuario_ocasional():
    """Retorna el contacto genérico 'Usuario Ocasional', creándolo si no existe."""
    ocasional = ClienteProveedor.query.filter_by(nit="0000000000").first()
    if not ocasional:
        ocasional = ClienteProveedor(
            nit                 = "0000000000",
            nombre              = "Usuario Ocasional",
            direccion           = "N/A",
            celular             = "0000000000",
            tipo                = "Cliente",
            tipo_identificacion = "NIT",
            correo              = None
        )
        db.session.add(ocasional)
        db.session.commit()
    return ocasional


def generar_comprobante_baja():
    """Genera un número de comprobante automático para bajas. Ej: BAJA-2026-A3F7"""
    año    = datetime.utcnow().year
    sufijo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"BAJA-{año}-{sufijo}"


def listar_movimiento():
    return Movimiento.query.order_by(
        Movimiento.fecha_creacion.desc()
    ).all()


def crear_movimiento(form):
    id_cliente = form.id_cliente.data
    id_insumo  = form.id_insumo.data
    tipo       = form.tipo.data
    precio     = float(form.precio.data)
    cantidad   = int(form.cantidad.data)

    if not id_cliente:
        raise ValueError("Debe seleccionar un cliente")
    if not id_insumo:
        raise ValueError("Debe seleccionar un insumo")
    if precio <= 0:
        raise ValueError("El precio debe ser mayor a 0")
    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor a 0")

    insumo = Insumo.query.get(id_insumo)
    if not insumo:
        raise ValueError("El insumo seleccionado no existe")

    if tipo == "entrada":
        insumo.cantidad += cantidad
    elif tipo == "salida":
        if insumo.cantidad < cantidad:
            raise ValueError(f"Stock insuficiente. Disponible: {insumo.cantidad}")
        insumo.cantidad -= cantidad
    elif tipo == "devolucion":
        insumo.cantidad += cantidad

    id_usuario     = session.get("id")
    nombre_usuario = session.get("nombre") or session.get("username") or "Desconocido"

    movimiento = Movimiento(
        id_cliente        = id_cliente,
        id_insumo         = id_insumo,
        id_usuario        = id_usuario,
        nombre_usuario    = nombre_usuario,
        tipo              = tipo,
        precio            = precio,
        cantidad          = cantidad,
        observaciones     = form.observaciones.data or "",
        fecha_vencimiento = form.fecha_vencimiento.data or None
    )

    db.session.add(movimiento)
    db.session.commit()
    return movimiento


def crear_movimientos_multiple(request_form):
    """
    Crea múltiples movimientos desde un POST con productos en lista.
    Espera campos: id_cliente, tipo, observaciones,
    productos[0][id_insumo], productos[0][precio], productos[0][cantidad],
    productos[0][fecha_vencimiento]
    """
    from flask import request as req

    tipo           = request_form.get("tipo", "salida")
    observaciones  = request_form.get("observaciones", "")
    es_ocasional   = request_form.get("es_ocasional") == "1"
    id_cliente_raw = request_form.get("id_cliente", "").strip()

    # Resolver cliente
    if es_ocasional or not id_cliente_raw:
        ocasional  = obtener_o_crear_usuario_ocasional()
        id_cliente = ocasional.id
    else:
        id_cliente = int(id_cliente_raw)

    id_usuario     = session.get("user_id")
    nombre_usuario = session.get("nombre") or session.get("username") or "Desconocido"

    # Recopilar productos dinámicos del formulario
    productos = []
    i = 0
    while True:
        id_insumo_raw = request_form.get(f"productos[{i}][id_insumo]")
        if not id_insumo_raw:
            break
        productos.append({
            "id_insumo"         : int(id_insumo_raw),
            "precio"            : float(request_form.get(f"productos[{i}][precio]", 0)),
            "cantidad"          : int(request_form.get(f"productos[{i}][cantidad]", 1)),
            "fecha_vencimiento" : request_form.get(f"productos[{i}][fecha_vencimiento]") or None,
        })
        i += 1

    if not productos:
        raise ValueError("Debe agregar al menos un producto")

    # Comprobante automático para bajas
    es_baja = tipo == "baja"
    if es_baja:
        comprobante = generar_comprobante_baja()
        tipo_real   = "salida"
    else:
        comprobante = request_form.get("numero", "").strip() or None
        tipo_real   = tipo

    movimientos_creados = []

    for p in productos:
        insumo = Insumo.query.get(p["id_insumo"])
        if not insumo:
            raise ValueError(f"Producto ID {p['id_insumo']} no existe")
        if p["precio"] <= 0:
            raise ValueError(f"El precio de '{insumo.descripcion}' debe ser mayor a 0")
        if p["cantidad"] <= 0:
            raise ValueError(f"La cantidad de '{insumo.descripcion}' debe ser mayor a 0")

        # Actualizar stock
        if tipo_real == "entrada":
            insumo.cantidad += p["cantidad"]
        elif tipo_real == "salida":
            if insumo.cantidad < p["cantidad"]:
                raise ValueError(
                    f"Stock insuficiente para '{insumo.descripcion}'. "
                    f"Disponible: {insumo.cantidad}"
                )
            insumo.cantidad -= p["cantidad"]
        elif tipo_real == "devolucion":
            insumo.cantidad += p["cantidad"]

        # Para bajas el precio es 0 (no es venta)
        precio_final = 0 if es_baja else p["precio"]

        # Parsear fecha_vencimiento
        fecha_venc = None
        if p["fecha_vencimiento"]:
            try:
                fecha_venc = datetime.strptime(p["fecha_vencimiento"], "%Y-%m-%d").date()
            except ValueError:
                fecha_venc = None

        mov = Movimiento(
            id_cliente        = id_cliente,
            id_insumo         = p["id_insumo"],
            id_usuario        = id_usuario,
            nombre_usuario    = nombre_usuario,
            tipo              = "baja" if es_baja else tipo_real,
            precio            = precio_final,
            cantidad          = p["cantidad"],
            observaciones     = f"[{comprobante}] {observaciones}" if comprobante else observaciones,
            fecha_vencimiento = fecha_venc
        )
        db.session.add(mov)
        movimientos_creados.append(mov)

    db.session.commit()
    return movimientos_creados


def obtener_movimiento(id):
    return Movimiento.query.get_or_404(id)


def editar_movimiento(id, form):
    movimiento = Movimiento.query.get_or_404(id)

    id_cliente = form.id_cliente.data
    id_insumo  = form.id_insumo.data
    tipo       = form.tipo.data
    precio     = float(form.precio.data)
    cantidad   = int(form.cantidad.data)

    if not id_cliente:
        raise ValueError("Debe seleccionar un cliente")
    if not id_insumo:
        raise ValueError("Debe seleccionar un insumo")
    if precio <= 0:
        raise ValueError("El precio debe ser mayor a 0")
    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor a 0")

    insumo = Insumo.query.get(movimiento.id_insumo)
    if insumo:
        if movimiento.tipo == "entrada":
            insumo.cantidad -= movimiento.cantidad
        elif movimiento.tipo in ("salida", "baja"):
            insumo.cantidad += movimiento.cantidad
        elif movimiento.tipo == "devolucion":
            insumo.cantidad -= movimiento.cantidad

    nuevo_insumo = Insumo.query.get(id_insumo)
    if not nuevo_insumo:
        raise ValueError("El insumo seleccionado no existe")

    if tipo == "entrada":
        nuevo_insumo.cantidad += cantidad
    elif tipo == "salida":
        if nuevo_insumo.cantidad < cantidad:
            raise ValueError(f"Stock insuficiente. Disponible: {nuevo_insumo.cantidad}")
        nuevo_insumo.cantidad -= cantidad
    elif tipo == "devolucion":
        nuevo_insumo.cantidad += cantidad

    movimiento.id_cliente        = id_cliente
    movimiento.id_insumo         = id_insumo
    movimiento.tipo              = tipo
    movimiento.precio            = precio
    movimiento.cantidad          = cantidad
    movimiento.observaciones     = form.observaciones.data or ""
    movimiento.fecha_vencimiento = form.fecha_vencimiento.data or None

    db.session.commit()
    return movimiento


def eliminar_movimiento(id):
    movimiento = Movimiento.query.get_or_404(id)

    insumo = Insumo.query.get(movimiento.id_insumo)
    if insumo:
        if movimiento.tipo == "entrada":
            insumo.cantidad -= movimiento.cantidad
        elif movimiento.tipo in ("salida", "baja"):
            insumo.cantidad += movimiento.cantidad
        elif movimiento.tipo == "devolucion":
            insumo.cantidad -= movimiento.cantidad

    db.session.delete(movimiento)
    db.session.commit()
    return True