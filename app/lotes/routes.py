from flask import render_template, request, redirect, url_for, flash, session
from . import lotes_bp
from .services import crear_lote, listar_lotes_por_insumo, obtener_lote, eliminar_lote
from app.insumos.models import Insumo
from app.clienteproveedor.models import ClienteProveedor
from datetime import datetime


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@lotes_bp.route('/insumo/<int:id_insumo>')
@login_required
def index(id_insumo):
    insumo    = Insumo.query.get_or_404(id_insumo)
    lotes     = listar_lotes_por_insumo(id_insumo)
    proveedores = ClienteProveedor.query.filter_by(tipo='P').all()
    prov_map  = {p.id: p.nombre for p in proveedores}

    total_unidades = sum(l.cantidad for l in lotes)
    por_vencer = sum(1 for l in lotes
                     if l.fecha_vencimiento and
                     (l.fecha_vencimiento - datetime.utcnow().date()).days <= 30
                     and l.fecha_vencimiento >= datetime.utcnow().date())
    vencidos = sum(1 for l in lotes
                   if l.fecha_vencimiento and
                   l.fecha_vencimiento < datetime.utcnow().date())

    return render_template('lotes/index.html',
                           insumo=insumo,
                           lotes=lotes,
                           prov_map=prov_map,
                           total_unidades=total_unidades,
                           por_vencer=por_vencer,
                           vencidos=vencidos)


@lotes_bp.route('/insumo/<int:id_insumo>/nuevo', methods=['GET', 'POST'])
@login_required
def crear(id_insumo):
    insumo      = Insumo.query.get_or_404(id_insumo)
    proveedores = ClienteProveedor.query.filter_by(tipo='P').all()

    if request.method == 'POST':
        try:
            fecha_venc    = request.form.get('fecha_vencimiento')
            fecha_entrada = request.form.get('fecha_entrada')

            data = {
                'id_insumo':        id_insumo,
                'id_proveedor':     request.form.get('id_proveedor') or None,
                'numero_lote':      request.form.get('numero_lote'),
                'cantidad':         request.form.get('cantidad', 0),
                'costo_compra':     request.form.get('costo_compra') or 0,
                'fecha_vencimiento':datetime.strptime(fecha_venc, '%Y-%m-%d').date()
                                    if fecha_venc else None,
                'fecha_entrada':    datetime.strptime(fecha_entrada, '%Y-%m-%d')
                                    if fecha_entrada else datetime.utcnow(),
            }
            crear_lote(data)
            flash(f'Lote registrado exitosamente para {insumo.descripcion}', 'success')
            return redirect(url_for('lotes.index', id_insumo=id_insumo))
        except Exception as e:
            flash(f'Error al registrar lote: {str(e)}', 'danger')

    return render_template('lotes/create.html',
                           insumo=insumo,
                           proveedores=proveedores)


@lotes_bp.route('/<int:lote_id>/eliminar', methods=['POST'])
@login_required
def eliminar(lote_id):
    lote = obtener_lote(lote_id)
    id_insumo = lote.id_insumo
    eliminar_lote(lote_id)
    flash('Lote eliminado correctamente', 'info')
    return redirect(url_for('lotes.index', id_insumo=id_insumo))