from flask import render_template, request, redirect, url_for, flash, session, jsonify
from datetime import date
import json
from . import insumos_bp
from app.insumos.forms import InsumoForm
from app.insumos.services import (
    crear_insumo, actualizar_insumo, eliminar_insumo, inactivar_insumo,
    listar_todos_insumos, obtener_insumo,
    buscar_insumos, obtener_insumo_por_codigo
)
from app.insumos.models import Insumo
from app.auth.routes import login_required, admin_required


@insumos_bp.route("/")
@login_required
def index():
    todos      = listar_todos_insumos()
    hoy        = date.today()
    es_admin   = session.get("rol") == "admin"
    por_vencer = sum(1 for i in todos
                     if i.activo and i.fecha_vencimiento and hoy <= i.fecha_vencimiento
                     and (i.fecha_vencimiento - hoy).days <= 30)
    stock_bajo = sum(1 for i in todos if i.activo and i.cantidad <= i.stock_minimo)
    insumos_json = json.dumps([{
        'id':                i.id,
        'codigo':            i.codigo,
        'descripcion':       i.descripcion,
        'lote':              i.lote or '',
        'invima':            i.invima or '',
        'valor':             float(i.valor),
        'iva':               float(i.iva) if i.iva else 0,
        'cantidad':          i.cantidad,
        'fecha_vencimiento': i.fecha_vencimiento.strftime('%d/%m/%Y') if i.fecha_vencimiento else '',
        'activo':            i.activo
    } for i in todos])
    return render_template("insumos/index.html",
                           insumos=todos,
                           today=hoy,
                           es_admin=es_admin,
                           por_vencer=por_vencer,
                           stock_bajo=stock_bajo,
                           insumos_json=insumos_json)


@insumos_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = InsumoForm()
    if form.validate_on_submit():
        try:
            crear_insumo(form)
            flash("Insumo creado correctamente", "success")
            return redirect(url_for("insumos.index"))
        except ValueError as e:
            flash(str(e), "danger")
    return render_template("insumos/create.html", form=form)


@insumos_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def edit(id):
    insumo = obtener_insumo(id)
    form   = InsumoForm(obj=insumo)
    if form.validate_on_submit():
        try:
            actualizar_insumo(id, form)
            flash("Insumo actualizado correctamente", "success")
            return redirect(url_for("insumos.index"))
        except ValueError as e:
            flash(str(e), "danger")
    return render_template("insumos/edit.html", form=form, insumo=insumo)


@insumos_bp.route('/inactivar/<int:id>', methods=['POST'])
@admin_required
def inactivar(id):
    inactivar_insumo(id)
    flash('Insumo inactivado correctamente', 'warning')
    return redirect(url_for('insumos.index'))


@insumos_bp.route("/delete/<int:id>", methods=["GET", "POST"])
@admin_required
def delete(id):
    insumo = obtener_insumo(id)
    return render_template("insumos/delete.html", insumo=insumo)


@insumos_bp.route("/delete/<int:id>/confirm", methods=["POST"])
@admin_required
def delete_confirm(id):
    try:
        eliminar_insumo(id)
        flash("Insumo eliminado correctamente", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("insumos.index"))


# === API ===

@insumos_bp.route('/api/insumos')
def api_listar_insumos():
    insumos = listar_todos_insumos()
    return jsonify([{
        "id": i.id, "codigo": i.codigo, "descripcion": i.descripcion,
        "lote": i.lote, "invima": i.invima, "valor": float(i.valor),
        "iva": float(i.iva) if i.iva else 0,
        "fecha_vencimiento": i.fecha_vencimiento.isoformat() if i.fecha_vencimiento else None,
        "activo": i.activo
    } for i in insumos])


@insumos_bp.route('/api/insumos/buscar')
def api_buscar_insumos():
    query   = request.args.get('q', '')
    insumos = buscar_insumos(query)
    return jsonify([{
        "id": i.id, "codigo": i.codigo, "descripcion": i.descripcion,
        "lote": i.lote, "invima": i.invima, "valor": float(i.valor),
        "iva": float(i.iva) if i.iva else 0,
        "fecha_vencimiento": i.fecha_vencimiento.isoformat() if i.fecha_vencimiento else None,
        "activo": i.activo
    } for i in insumos])


@insumos_bp.route('/api/insumos/codigo/<codigo>')
def api_insumo_por_codigo(codigo):
    insumo = obtener_insumo_por_codigo(codigo)
    if not insumo:
        return jsonify({"error": "Insumo no encontrado"}), 404
    return jsonify({
        "id": insumo.id, "codigo": insumo.codigo, "descripcion": insumo.descripcion,
        "lote": insumo.lote, "invima": insumo.invima, "valor": float(insumo.valor),
        "iva": float(insumo.iva) if insumo.iva else 0,
        "fecha_vencimiento": insumo.fecha_vencimiento.isoformat() if insumo.fecha_vencimiento else None
    })