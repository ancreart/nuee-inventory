import json
from flask import render_template, request, redirect, url_for, flash, jsonify, session
from . import facturas_bp
from .forms import FacturaForm
from .services import crear_factura
from .models import Factura, FacturaDetalle
from app.clienteproveedor.models import ClienteProveedor
from app.insumos.models import Insumo
from app.extensions import db
from app.auth.routes import login_required, admin_required


@facturas_bp.route('/')
@login_required
def index():
    facturas         = Factura.query.order_by(Factura.id.desc()).all()
    clientes         = {c.id: c for c in ClienteProveedor.query.all()}
    total_facturas   = len(facturas)
    total_pagadas    = sum(1 for f in facturas if f.estado == 'Pagada')
    total_pendientes = sum(1 for f in facturas if f.estado == 'Pendiente')
    total_anuladas   = sum(1 for f in facturas if f.estado == 'Anulada')
    return render_template('facturas/index.html',
                           facturas=facturas,
                           clientes=clientes,
                           total_facturas=total_facturas,
                           total_pagadas=total_pagadas,
                           total_pendientes=total_pendientes,
                           total_anuladas=total_anuladas)


@facturas_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
def nueva():
    form     = FacturaForm()
    clientes = ClienteProveedor.query.all()
    insumos  = Insumo.query.filter_by(activo=True).all()

    if request.method == 'POST':
        id_cliente    = request.form.get('id_cliente')
        observaciones = request.form.get('observaciones', '')
        ids           = request.form.getlist('id_insumo[]')
        cantidades    = request.form.getlist('cantidad[]')
        precios       = request.form.getlist('precio_unitario[]')
        ivas          = request.form.getlist('iva[]')
        descripciones = request.form.getlist('descripcion[]')

        if not id_cliente or not ids:
            flash('Seleccione un cliente y al menos un producto', 'danger')
            return redirect(url_for('facturas.nueva'))

        items = []
        for i in range(len(ids)):
            items.append({
                'id_insumo':       ids[i],
                'descripcion':     descripciones[i],
                'cantidad':        cantidades[i],
                'precio_unitario': precios[i],
                'iva':             ivas[i] if ivas[i] else 0
            })
        try:
            factura = crear_factura(int(id_cliente), items, observaciones)
            flash(f'Factura {factura.numero} creada exitosamente', 'success')
            return redirect(url_for('facturas.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear factura: {str(e)}', 'danger')
            return redirect(url_for('facturas.nueva'))

    clientes_json = json.dumps([{
        'id':                  c.id,
        'nombre':              c.nombre,
        'nit':                 c.nit,
        'direccion':           c.direccion,
        'celular':             c.celular,
        'correo':              c.correo or '',
        'tipo_identificacion': c.tipo_identificacion or 'NIT',
        'tipo':                c.tipo
    } for c in clientes])

    insumos_json = json.dumps([{
        'id':          ins.id,
        'descripcion': ins.descripcion,
        'valor':       float(ins.valor),
        'iva':         float(ins.iva),
        'stock':       ins.cantidad
    } for ins in insumos])

    return render_template('facturas/nueva.html',
                           form=form,
                           clientes=clientes,
                           clientes_json=clientes_json,
                           insumos_json=insumos_json)


@facturas_bp.route('/<int:id>/estado', methods=['POST'])
@admin_required
def cambiar_estado(id):
    factura      = Factura.query.get_or_404(id)
    nuevo_estado = request.form.get('estado')
    if nuevo_estado in ['Pendiente', 'Pagada', 'Anulada']:
        factura.estado = nuevo_estado
        db.session.commit()
        flash(f'Estado actualizado a {nuevo_estado}', 'success')
    return redirect(url_for('facturas.index'))


@facturas_bp.route('/<int:id>/eliminar', methods=['POST'])
@admin_required
def eliminar(id):
    factura = Factura.query.get_or_404(id)
    db.session.delete(factura)
    db.session.commit()
    flash(f'Factura {factura.numero} eliminada', 'info')
    return redirect(url_for('facturas.index'))


@facturas_bp.route('/api/insumo/<int:id>')
@login_required
def api_insumo(id):
    insumo = Insumo.query.get_or_404(id)
    return jsonify({
        'id':          insumo.id,
        'descripcion': insumo.descripcion,
        'valor':       float(insumo.valor),
        'iva':         float(insumo.iva),
        'stock':       insumo.cantidad
    })