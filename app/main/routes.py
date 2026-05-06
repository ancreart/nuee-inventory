from flask import render_template, redirect, url_for, session
from . import main_bp
from app.insumos.models import Insumo
from app.clienteproveedor.models import ClienteProveedor
from app.movimientos.models import Movimiento
from datetime import date, timedelta
from sqlalchemy import func
from app.extensions import db


@main_bp.route("/")
def home():
    return redirect(url_for("auth.login"))


@main_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    hoy        = date.today()
    en_30_dias = hoy + timedelta(days=30)

    # ── Stats reales ──
    total_insumos   = Insumo.query.filter_by(activo=True).count()
    total_clientes  = ClienteProveedor.query.filter_by(tipo='C').count()
    movimientos_hoy = Movimiento.query.filter(
        Movimiento.fecha_creacion >= hoy
    ).count()

    # ── Alertas ──
    stock_bajo = Insumo.query.filter(
        Insumo.activo == True,
        Insumo.cantidad <= 5
    ).all()

    por_vencer = Insumo.query.filter(
        Insumo.activo == True,
        Insumo.fecha_vencimiento != None,
        Insumo.fecha_vencimiento <= en_30_dias,
        Insumo.fecha_vencimiento >= hoy
    ).all()

    vencidos = Insumo.query.filter(
        Insumo.activo == True,
        Insumo.fecha_vencimiento != None,
        Insumo.fecha_vencimiento < hoy
    ).all()

    # ── Últimos movimientos con nombre de insumo ──
    ultimos_movimientos = Movimiento.query.order_by(
        Movimiento.fecha_creacion.desc()
    ).limit(5).all()

    insumos_map = {i.id: i.descripcion for i in Insumo.query.all()}

    # ── Datos gráfica: movimientos últimos 7 días ──
    chart_labels   = []
    chart_entradas = []
    chart_salidas  = []

    for i in range(6, -1, -1):
        dia = hoy - timedelta(days=i)
        dia_siguiente = dia + timedelta(days=1)

        entradas = Movimiento.query.filter(
            Movimiento.tipo == 'entrada',
            Movimiento.fecha_creacion >= dia,
            Movimiento.fecha_creacion < dia_siguiente
        ).count()

        salidas = Movimiento.query.filter(
            Movimiento.tipo == 'salida',
            Movimiento.fecha_creacion >= dia,
            Movimiento.fecha_creacion < dia_siguiente
        ).count()

        chart_labels.append(dia.strftime('%d/%m'))
        chart_entradas.append(entradas)
        chart_salidas.append(salidas)

    # ── Top 5 insumos más vendidos (por cantidad total en salidas) ──
    top_query = db.session.query(
        Insumo.descripcion,
        func.sum(Movimiento.cantidad).label('total')
    ).join(
        Movimiento, Movimiento.id_insumo == Insumo.id
    ).filter(
        Movimiento.tipo == 'salida'
    ).group_by(
        Insumo.id, Insumo.descripcion
    ).order_by(
        func.sum(Movimiento.cantidad).desc()
    ).limit(5).all()

    top_insumos = [{'descripcion': row.descripcion, 'total': row.total} for row in top_query]

    return render_template("main/dashboard.html",
        total_insumos=total_insumos,
        total_clientes=total_clientes,
        movimientos_hoy=movimientos_hoy,
        stock_bajo=stock_bajo,
        por_vencer=por_vencer,
        vencidos=vencidos,
        ultimos_movimientos=ultimos_movimientos,
        insumos_map=insumos_map,
        hoy=hoy,
        chart_labels=chart_labels,
        chart_entradas=chart_entradas,
        chart_salidas=chart_salidas,
        top_insumos=top_insumos,
    )