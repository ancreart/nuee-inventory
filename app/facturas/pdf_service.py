"""
app/facturas/pdf_service.py — v2
Genera el PDF de una factura de Nuée usando ReportLab.
"""

import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER


# ── Paleta Nuée ──────────────────────────────────────────────
COLOR_BLACK   = colors.HexColor('#111111')
COLOR_GRAY    = colors.HexColor('#666666')
COLOR_LIGHT   = colors.HexColor('#F5F5F5')
COLOR_BORDER  = colors.HexColor('#E8E8E8')
COLOR_WHITE   = colors.white
COLOR_SUCCESS = colors.HexColor('#3B6D11')


def _draw_logo(c, x, y, size=28):
    """
    Dibuja el logo Nuée (nube + gota) usando primitivas de ReportLab.
    ReportLab tiene Y invertido respecto al SVG — se espeja cada coordenada:
    y_pdf = y_base + (32 - y_svg) * scale
    """
    scale = size / 32

    def sy(y_svg):
        """Convierte coordenada Y del SVG (origen arriba) a PDF (origen abajo)."""
        return y + (32 - y_svg) * scale

    # Fondo blanco redondeado
    c.setFillColor(COLOR_WHITE)
    c.setStrokeColor(COLOR_BORDER)
    c.setLineWidth(0.5)
    pad = size * 0.15
    c.roundRect(x - pad, y - pad, size + pad * 2, size + pad * 2,
                radius=4, fill=1, stroke=1)

    # Nube
    c.setStrokeColor(COLOR_BLACK)
    c.setFillColor(COLOR_WHITE)
    c.setLineWidth(1.5 * scale)
    c.setLineCap(1)

    p = c.beginPath()
    p.moveTo(x + 10 * scale, sy(19.45))
    p.curveTo(x + 6.46 * scale, sy(19.45),
              x + 5 * scale,    sy(17.99),
              x + 5 * scale,    sy(16.2))
    p.curveTo(x + 5 * scale,    sy(16.2),
              x + 6.07 * scale, sy(13.35),
              x + 7.51 * scale, sy(13))
    p.curveTo(x + 7.5 * scale,  sy(13),
              x + 7.5 * scale,  sy(12.78),
              x + 7.5 * scale,  sy(12.67))
    p.curveTo(x + 7.5 * scale,  sy(12.67),
              x + 10.04 * scale, sy(7),
              x + 13.17 * scale, sy(7))
    p.curveTo(x + 13.17 * scale, sy(7),
              x + 17.42 * scale, sy(8.39),
              x + 18.25 * scale, sy(10.36))
    p.curveTo(x + 18.79 * scale, sy(10.13),
              x + 19.38 * scale, sy(10),
              x + 20 * scale,    sy(10))
    p.curveTo(x + 20 * scale,    sy(10),
              x + 24.5 * scale,  sy(12.01),
              x + 24.5 * scale,  sy(14.5))
    c.drawPath(p, fill=0, stroke=1)

    # Gota
    c.setFillColor(COLOR_BLACK)
    c.setStrokeColor(COLOR_BLACK)
    c.setLineWidth(0)
    p2 = c.beginPath()
    p2.moveTo(x + 16 * scale, sy(13))
    p2.curveTo(x + 16 * scale, sy(13),
               x + 11 * scale, sy(18.5),
               x + 11 * scale, sy(21.5))
    p2.curveTo(x + 11 * scale,    sy(21.5),
               x + 13.24 * scale, sy(26),
               x + 16 * scale,    sy(26))
    p2.curveTo(x + 16 * scale,    sy(26),
               x + 18.76 * scale, sy(26),
               x + 21 * scale,    sy(21.5))
    p2.curveTo(x + 21 * scale, sy(21.5),
               x + 16 * scale, sy(13),
               x + 16 * scale, sy(13))
    c.drawPath(p2, fill=1, stroke=0)

    # Reflejo en la gota
    c.setStrokeColor(COLOR_WHITE)
    c.setLineWidth(1 * scale)
    c.setLineCap(1)
    p3 = c.beginPath()
    p3.moveTo(x + 13.5 * scale, sy(21))
    p3.curveTo(x + 13.5 * scale, sy(21),
               x + 14.8 * scale, sy(17.8),
               x + 15.5 * scale, sy(16.8))
    c.drawPath(p3, fill=0, stroke=1)


def generar_pdf_factura(factura, cliente, detalles):
    """
    Genera el PDF de una factura y lo devuelve como bytes.

    Args:
        factura:  objeto Factura del modelo
        cliente:  objeto ClienteProveedor
        detalles: lista de FacturaDetalle

    Returns:
        bytes del PDF generado
    """
    buffer = io.BytesIO()
    w, h = A4  # 595.27 x 841.89 pts
    c = pdf_canvas.Canvas(buffer, pagesize=A4)

    margin_x = 40
    margin_top = h - 40

    # ── HEADER ────────────────────────────────────────────────
    # Fondo oscuro del header
    c.setFillColor(COLOR_BLACK)
    c.rect(0, h - 90, w, 90, fill=1, stroke=0)

    # Logo
    _draw_logo(c, x=margin_x, y=h - 78, size=52)

    # Nombre Nuée — Tenor Sans no disponible en PDF, usamos Helvetica-Oblique
    c.setFillColor(COLOR_WHITE)
    c.setFont('Helvetica', 22)
    c.drawString(margin_x + 70, h - 48, 'Nu\xe9e')

    c.setFillColor(colors.HexColor('#888888'))
    c.setFont('Helvetica', 7)
    c.drawString(margin_x + 71, h - 62, 'SKINCARE MANAGEMENT')

    # Número de factura (derecha)
    c.setFillColor(COLOR_WHITE)
    c.setFont('Helvetica-Bold', 14)
    num_w = c.stringWidth(factura.numero, 'Helvetica-Bold', 14)
    c.drawString(w - margin_x - num_w, h - 45, factura.numero)

    c.setFillColor(colors.HexColor('#888888'))
    c.setFont('Helvetica', 8)
    label = 'FACTURA DE VENTA'
    label_w = c.stringWidth(label, 'Helvetica', 8)
    c.drawString(w - margin_x - label_w, h - 60, label)

    # ── INFO FACTURA + CLIENTE ────────────────────────────────
    y = margin_top - 110

    # Columna izquierda: datos del cliente
    c.setFillColor(COLOR_BLACK)
    c.setFont('Helvetica-Bold', 8)
    c.drawString(margin_x, y, 'FACTURAR A')

    y -= 16
    c.setFont('Helvetica-Bold', 11)
    c.drawString(margin_x, y, cliente.nombre)

    y -= 14
    c.setFillColor(COLOR_GRAY)
    c.setFont('Helvetica', 9)

    tipo_id = getattr(cliente, 'tipo_identificacion', 'NIT') or 'NIT'
    c.drawString(margin_x, y, f'{tipo_id}: {cliente.nit}')

    y -= 12
    if cliente.direccion:
        c.drawString(margin_x, y, cliente.direccion)
        y -= 12

    if cliente.celular:
        c.drawString(margin_x, y, f'Tel: {cliente.celular}')
        y -= 12

    if cliente.correo:
        c.drawString(margin_x, y, cliente.correo)

    # Columna derecha: datos de la factura
    col2_x = w / 2 + 20
    y_right = margin_top - 126

    datos_factura = [
        ('Fecha',      factura.fecha.strftime('%d/%m/%Y') if factura.fecha else '—'),
        ('Estado',     factura.estado),
        ('Registrado', factura.nombre_usuario or '—'),
    ]
    if factura.observaciones:
        datos_factura.append(('Observaciones', factura.observaciones))

    for label, valor in datos_factura:
        c.setFillColor(COLOR_GRAY)
        c.setFont('Helvetica', 8)
        c.drawString(col2_x, y_right, label.upper())
        c.setFillColor(COLOR_BLACK)
        c.setFont('Helvetica', 9)
        c.drawString(col2_x + 90, y_right, str(valor))
        y_right -= 14

    # ── SEPARADOR ────────────────────────────────────────────
    y_table = min(y, y_right) - 20
    c.setStrokeColor(COLOR_BORDER)
    c.setLineWidth(0.5)
    c.line(margin_x, y_table, w - margin_x, y_table)

    # ── TABLA DE PRODUCTOS ────────────────────────────────────
    y_table -= 14
    col_desc  = margin_x
    col_cant  = w - margin_x - 180
    col_precio = w - margin_x - 110
    col_iva   = w - margin_x - 60
    col_sub   = w - margin_x

    # Encabezado tabla
    c.setFillColor(COLOR_LIGHT)
    c.rect(margin_x, y_table - 4, w - margin_x * 2, 20, fill=1, stroke=0)

    c.setFillColor(COLOR_GRAY)
    c.setFont('Helvetica-Bold', 7.5)
    c.drawString(col_desc, y_table + 4, 'PRODUCTO')
    c.drawRightString(col_cant,   y_table + 4, 'CANT.')
    c.drawRightString(col_precio, y_table + 4, 'P. UNIT.')
    c.drawRightString(col_iva,    y_table + 4, 'IVA %')
    c.drawRightString(col_sub,    y_table + 4, 'SUBTOTAL')

    y_table -= 20
    c.setStrokeColor(COLOR_BORDER)
    c.setLineWidth(0.3)

    # Filas de productos
    for i, det in enumerate(detalles):
        if i % 2 == 0:
            c.setFillColor(colors.HexColor('#FAFAFA'))
            c.rect(margin_x, y_table - 4, w - margin_x * 2, 18, fill=1, stroke=0)

        c.setFillColor(COLOR_BLACK)
        c.setFont('Helvetica', 8.5)

        # Descripción con truncado
        desc = det.descripcion
        if len(desc) > 45:
            desc = desc[:42] + '...'
        c.drawString(col_desc, y_table + 2, desc)

        c.setFont('Helvetica', 8.5)
        c.drawRightString(col_cant,   y_table + 2, str(det.cantidad))
        c.drawRightString(col_precio, y_table + 2,
                         f'${float(det.precio_unitario):,.0f}')
        c.drawRightString(col_iva,    y_table + 2,
                         f'{float(det.iva):.0f}%')
        c.setFont('Helvetica-Bold', 8.5)
        c.drawRightString(col_sub,    y_table + 2,
                         f'${float(det.subtotal):,.0f}')

        c.setStrokeColor(COLOR_BORDER)
        c.line(margin_x, y_table - 4, w - margin_x, y_table - 4)
        y_table -= 18

    # ── TOTALES ───────────────────────────────────────────────
    y_table -= 10
    totales_x = w - margin_x - 180
    totales_val = w - margin_x

    def _fila_total(label, valor, bold=False, grande=False):
        nonlocal y_table
        font = 'Helvetica-Bold' if bold else 'Helvetica'
        size = 10 if grande else 8.5
        c.setFillColor(COLOR_GRAY if not bold else COLOR_BLACK)
        c.setFont(font, size)
        c.drawString(totales_x, y_table, label)
        c.setFillColor(COLOR_BLACK)
        c.setFont(font, size)
        c.drawRightString(totales_val, y_table, valor)
        y_table -= (14 if not grande else 18)

    _fila_total('Subtotal:', f'${float(factura.subtotal):,.2f}')
    _fila_total('IVA:', f'${float(factura.total_iva):,.2f}')

    # Línea antes del total
    c.setStrokeColor(COLOR_BLACK)
    c.setLineWidth(0.5)
    c.line(totales_x, y_table + 10, totales_val, y_table + 10)
    y_table -= 4

    _fila_total('TOTAL:', f'${float(factura.total):,.2f}', bold=True, grande=True)

    # ── FOOTER ────────────────────────────────────────────────
    footer_y = 35
    c.setFillColor(COLOR_LIGHT)
    c.rect(0, 0, w, footer_y + 10, fill=1, stroke=0)

    c.setFillColor(COLOR_GRAY)
    c.setFont('Helvetica', 7.5)
    footer_text = 'Nu\xe9e Skincare Management  \xb7  Documento generado electr\xf3nicamente'
    fw = c.stringWidth(footer_text, 'Helvetica', 7.5)
    c.drawString((w - fw) / 2, footer_y - 6, footer_text)

    c.setFont('Helvetica-Bold', 7.5)
    num_w2 = c.stringWidth(factura.numero, 'Helvetica-Bold', 7.5)
    c.drawString((w - num_w2) / 2, footer_y + 6, factura.numero)

    c.save()
    buffer.seek(0)
    return buffer.getvalue()