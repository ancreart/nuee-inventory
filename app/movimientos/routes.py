from flask import render_template, request, redirect, url_for, flash, jsonify, session
from . import movimientos_bp
from app.movimientos.forms import MovimientoForm
from app.movimientos.services import (
    listar_movimiento, crear_movimiento, crear_movimientos_multiple,
    editar_movimiento, eliminar_movimiento, obtener_movimiento
)
from app.clienteproveedor.services import buscar_clientes, listar_clientes, obtener_cliente_por_nit
from app.insumos.services import buscar_insumos, listar_insumos_activos, obtener_insumo_por_codigo
from app.clienteproveedor.models import ClienteProveedor
from app.insumos.models import Insumo
from app.auth.routes import login_required, admin_required


@movimientos_bp.route("/")
@login_required
def index():
    movimientos = listar_movimiento()
    clientes    = {c.id: c.nombre for c in ClienteProveedor.query.all()}
    insumos     = {i.id: i.descripcion for i in Insumo.query.all()}
    es_admin    = session.get("rol") == "admin"
    return render_template("movimientos/index.html",
                           movimientos=movimientos,
                           clientes=clientes,
                           insumos=insumos,
                           es_admin=es_admin)


@movimientos_bp.route("/crear", methods=["GET", "POST"])
@login_required
def crear():
    form = MovimientoForm()
    if request.method == "POST":
        try:
            crear_movimientos_multiple(request.form)
            flash("Movimiento registrado correctamente", "success")
            return redirect(url_for("movimientos.index"))
        except ValueError as e:
            flash(str(e), "danger")
    return render_template("movimientos/create.html", form=form)


@movimientos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@admin_required
def editar(id):
    movimiento = obtener_movimiento(id)
    form = MovimientoForm(obj=movimiento)
    if form.validate_on_submit():
        try:
            editar_movimiento(id, form)
            flash("Movimiento actualizado correctamente", "success")
            return redirect(url_for("movimientos.index"))
        except ValueError as e:
            flash(str(e), "danger")
    return render_template("movimientos/edit.html", movimiento=movimiento, form=form)


@movimientos_bp.route("/eliminar/<int:id>", methods=["POST"])
@admin_required
def eliminar(id):
    try:
        eliminar_movimiento(id)
        flash("Movimiento eliminado correctamente", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("movimientos.index"))


# === API ===

@movimientos_bp.route("/api/clientes")
def api_listar_clientes():
    clientes = listar_clientes()
    return jsonify([{"id": c.id, "nit": c.nit, "nombre": c.nombre,
                     "direccion": c.direccion, "telefono": c.celular, "tipo": c.tipo}
                    for c in clientes])


@movimientos_bp.route("/api/clientes/buscar")
def api_buscar_clientes():
    query    = request.args.get('q', '')
    clientes = buscar_clientes(query)
    return jsonify([{"id": c.id, "nit": c.nit, "nombre": c.nombre,
                     "direccion": c.direccion, "telefono": c.celular, "tipo": c.tipo}
                    for c in clientes])


@movimientos_bp.route("/api/clientes/nit/<nit>")
def api_cliente_por_nit(nit):
    cliente = obtener_cliente_por_nit(nit)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404
    return jsonify({"id": cliente.id, "nit": cliente.nit, "nombre": cliente.nombre,
                    "direccion": cliente.direccion, "telefono": cliente.celular})


@movimientos_bp.route("/api/insumos")
def api_listar_insumos():
    insumos = listar_insumos_activos()
    return jsonify([{
        "id"               : i.id,
        "codigo"           : i.codigo,
        "descripcion"      : i.descripcion,
        "lote"             : i.lote,
        "invima"           : i.invima,
        "valor"            : float(i.valor),
        "iva"              : float(i.iva) if i.iva else 0,
        "stock"            : i.cantidad,
        "fecha_vencimiento": i.fecha_vencimiento.isoformat() if i.fecha_vencimiento else None
    } for i in insumos])


@movimientos_bp.route("/api/insumos/buscar")
def api_buscar_insumos():
    query   = request.args.get('q', '')
    insumos = buscar_insumos(query)
    return jsonify([{
        "id"               : i.id,
        "codigo"           : i.codigo,
        "descripcion"      : i.descripcion,
        "lote"             : i.lote,
        "invima"           : i.invima,
        "valor"            : float(i.valor),
        "iva"              : float(i.iva) if i.iva else 0,
        "stock"            : i.cantidad,
        "fecha_vencimiento": i.fecha_vencimiento.isoformat() if i.fecha_vencimiento else None
    } for i in insumos])


@movimientos_bp.route("/api/insumos/codigo/<codigo>")
def api_insumo_por_codigo(codigo):
    insumo = obtener_insumo_por_codigo(codigo)
    if not insumo:
        return jsonify({"error": "Insumo no encontrado"}), 404
    return jsonify({
        "id"               : insumo.id,
        "codigo"           : insumo.codigo,
        "descripcion"      : insumo.descripcion,
        "lote"             : insumo.lote,
        "invima"           : insumo.invima,
        "valor"            : float(insumo.valor),
        "iva"              : float(insumo.iva) if insumo.iva else 0,
        "stock"            : insumo.cantidad,
        "fecha_vencimiento": insumo.fecha_vencimiento.isoformat() if insumo.fecha_vencimiento else None
    })