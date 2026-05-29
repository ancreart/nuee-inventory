"""
app/facturas/routes.py
Rutas de facturas: listado, nueva factura, cambio de estado,
creación de cliente inline, descarga de PDF y envío por correo.
"""

import json
from flask import (render_template, request, redirect, url_for,
                   flash, jsonify, session, make_response)
from . import facturas_bp
from .forms import FacturaForm
from .services import crear_factura
from .models import Factura, FacturaDetalle
from .pdf_service import generar_pdf_factura
from .email_service import enviar_factura_por_correo
from app.clienteproveedor.models import ClienteProveedor
from app.clienteproveedor.services import crear_cliente
from app.insumos.models import Insumo
from app.extensions import db, csrf
from app.auth.routes import login_required, admin_required


# ── Helper ────────────────────────────────────────────────────

def _serializar_clientes(clientes):
    return json.dumps([{
        'id':                  c.id,
        'nombre':              c.nombre,
        'nit':                 c.nit,
        'direccion':           c.direccion,
        'celular':             c.celular,
        'correo':              c.correo or '',
        'tipo_identificacion': c.tipo_identificacion or 'NIT',
        'tipo':                c.tipo
    } for c in clientes])


def _serializar_insumos(insumos):
    return json.dumps([{
        'id':          ins.id,
        'descripcion': ins.descripcion,
        'valor':       float(ins.valor),
        'iva':         float(ins.iva),
        'stock':       ins.cantidad
    } for ins in insumos])


# ── Listado ───────────────────────────────────────────────────

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


# ── Nueva factura ─────────────────────────────────────────────

@facturas_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
def nueva():
    form     = FacturaForm()
    clientes = ClienteProveedor.query.order_by(ClienteProveedor.nombre).all()
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
            flash('Seleccione un cliente y al menos un producto.', 'danger')
            return redirect(url_for('facturas.nueva'))

        items = []
        for i in range(len(ids)):
            items.append({
                'id_insumo':       ids[i],
                'descripcion':     descripciones[i],
                'cantidad':        cantidades[i],
                'precio_unitario': precios[i],
                'iva':             ivas[i] if i < len(ivas) and ivas[i] else 0
            })

        try:
            factura = crear_factura(int(id_cliente), items, observaciones)
            flash(f'Factura {factura.numero} creada exitosamente.', 'success')

            # Enviar PDF por correo si el cliente tiene correo
            cliente = ClienteProveedor.query.get(id_cliente)
            if cliente and cliente.correo:
                detalles = FacturaDetalle.query.filter_by(
                    id_factura=factura.id).all()
                ok, msg = enviar_factura_por_correo(factura, cliente, detalles)
                if ok:
                    flash(f'Factura enviada por correo a {cliente.correo}.', 'success')
                else:
                    flash(f'Factura creada pero no se pudo enviar: {msg}', 'warning')

            return redirect(url_for('facturas.index'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear factura: {str(e)}', 'danger')
            return redirect(url_for('facturas.nueva'))

    return render_template('facturas/nueva.html',
                           form=form,
                           clientes=clientes,
                           clientes_json=_serializar_clientes(clientes),
                           insumos_json=_serializar_insumos(insumos))


# ── Crear cliente inline ──────────────────────────────────────

@facturas_bp.route('/api/cliente/crear', methods=['POST'])
@csrf.exempt
@login_required
def api_crear_cliente():
    """
    Crea un cliente desde el modal de nueva factura.
    Devuelve el cliente creado en JSON para actualizar el dropdown sin recargar.
    CSRF exento porque recibe JSON, no form data.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos inválidos.'}), 400

    campos_requeridos = ['nit', 'nombre', 'direccion', 'celular', 'tipo']
    for campo in campos_requeridos:
        if not data.get(campo, '').strip():
            return jsonify({'error': f'El campo "{campo}" es obligatorio.'}), 400

    existente = ClienteProveedor.query.filter_by(
        nit=data['nit'].strip()).first()
    if existente:
        return jsonify({
            'error': f'Ya existe un contacto con el NIT {data["nit"]}.'
        }), 409

    try:
        nuevo = crear_cliente({
            'nit':                 data['nit'].strip(),
            'nombre':              data['nombre'].strip(),
            'direccion':           data['direccion'].strip(),
            'celular':             data['celular'].strip(),
            'tipo':                data['tipo'],
            'correo':              data.get('correo', '').strip(),
            'tipo_identificacion': data.get('tipo_identificacion', 'NIT')
        })
        return jsonify({
            'id':                  nuevo.id,
            'nombre':              nuevo.nombre,
            'nit':                 nuevo.nit,
            'direccion':           nuevo.direccion,
            'celular':             nuevo.celular,
            'correo':              nuevo.correo or '',
            'tipo_identificacion': nuevo.tipo_identificacion or 'NIT',
            'tipo':                nuevo.tipo
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ── Descargar PDF ─────────────────────────────────────────────

@facturas_bp.route('/<int:id>/pdf')
@login_required
def descargar_pdf(id):
    factura  = Factura.query.get_or_404(id)
    cliente  = ClienteProveedor.query.get(factura.id_cliente)
    detalles = FacturaDetalle.query.filter_by(id_factura=id).all()

    if not cliente:
        flash('No se encontró el cliente de esta factura.', 'danger')
        return redirect(url_for('facturas.index'))

    pdf_bytes = generar_pdf_factura(factura, cliente, detalles)

    response = make_response(pdf_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = \
        f'attachment; filename="{factura.numero}.pdf"'
    return response


# ── Reenviar por correo ───────────────────────────────────────

@facturas_bp.route('/<int:id>/enviar-correo', methods=['POST'])
@login_required
def enviar_correo(id):
    factura  = Factura.query.get_or_404(id)
    cliente  = ClienteProveedor.query.get(factura.id_cliente)
    detalles = FacturaDetalle.query.filter_by(id_factura=id).all()

    if not cliente:
        flash('No se encontró el cliente.', 'danger')
        return redirect(url_for('facturas.index'))

    ok, msg = enviar_factura_por_correo(factura, cliente, detalles)
    flash(msg, 'success' if ok else 'warning')
    return redirect(url_for('facturas.index'))


# ── Cambiar estado ────────────────────────────────────────────

@facturas_bp.route('/<int:id>/estado', methods=['POST'])
@admin_required
def cambiar_estado(id):
    factura      = Factura.query.get_or_404(id)
    nuevo_estado = request.form.get('estado')
    if nuevo_estado in ['Pendiente', 'Pagada', 'Anulada']:
        factura.estado = nuevo_estado
        db.session.commit()
        flash(f'Estado actualizado a {nuevo_estado}.', 'success')
    return redirect(url_for('facturas.index'))


# ── Eliminar ──────────────────────────────────────────────────

@facturas_bp.route('/<int:id>/eliminar', methods=['POST'])
@admin_required
def eliminar(id):
    factura = Factura.query.get_or_404(id)
    numero  = factura.numero
    db.session.delete(factura)
    db.session.commit()
    flash(f'Factura {numero} eliminada.', 'info')
    return redirect(url_for('facturas.index'))


# ── API insumo ────────────────────────────────────────────────

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