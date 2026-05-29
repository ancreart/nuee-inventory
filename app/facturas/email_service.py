"""
app/facturas/email_service.py
Envía la factura en PDF al correo del cliente.
"""

from flask import current_app
from flask_mail import Message
from app.extensions import mail
from app.facturas.pdf_service import generar_pdf_factura


def enviar_factura_por_correo(factura, cliente, detalles):
    """
    Genera el PDF de la factura y lo envía al correo del cliente.

    Returns:
        (bool, str): (éxito, mensaje)
    """
    if not cliente.correo:
        return False, 'El cliente no tiene correo registrado.'

    try:
        pdf_bytes = generar_pdf_factura(factura, cliente, detalles)

        asunto = f'Tu factura {factura.numero} — Nuée Skincare'

        cuerpo_html = f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    max-width: 520px; margin: 0 auto; padding: 40px 20px;
                    color: #111111; background: #FAFAFA;">

          <div style="text-align: center; margin-bottom: 32px;">
            <div style="display: inline-block; background: #111111;
                        padding: 12px 24px; border-radius: 10px;">
              <span style="font-size: 22px; color: #FFFFFF;
                           letter-spacing: 0.14em;">Nuée</span>
            </div>
          </div>

          <div style="background: #FFFFFF; border: 0.5px solid #E8E8E8;
                      border-radius: 14px; padding: 32px;">

            <h2 style="margin: 0 0 8px; font-size: 18px; font-weight: 600;">
              Hola, {cliente.nombre.split()[0]}
            </h2>
            <p style="margin: 0 0 24px; color: #666666; font-size: 14px;">
              Adjuntamos la factura correspondiente a tu compra en Nuée Skincare.
            </p>

            <div style="background: #F8F8F8; border-radius: 10px;
                        padding: 20px; margin-bottom: 24px;">
              <table style="width: 100%; border-collapse: collapse;">
                <tr>
                  <td style="color: #888888; font-size: 12px;
                             text-transform: uppercase; letter-spacing: 0.08em;
                             padding-bottom: 4px;">N° Factura</td>
                  <td style="text-align: right; font-weight: 600;
                             font-size: 14px;">{factura.numero}</td>
                </tr>
                <tr>
                  <td style="color: #888888; font-size: 12px;
                             text-transform: uppercase; letter-spacing: 0.08em;
                             padding-bottom: 4px;">Fecha</td>
                  <td style="text-align: right; font-size: 14px;">
                    {factura.fecha.strftime('%d/%m/%Y') if factura.fecha else '—'}
                  </td>
                </tr>
                <tr>
                  <td style="color: #888888; font-size: 12px;
                             text-transform: uppercase; letter-spacing: 0.08em;
                             padding-bottom: 4px;">Estado</td>
                  <td style="text-align: right; font-size: 14px;">{factura.estado}</td>
                </tr>
                <tr style="border-top: 0.5px solid #E8E8E8;">
                  <td style="font-weight: 700; font-size: 14px;
                             padding-top: 12px;">Total</td>
                  <td style="text-align: right; font-weight: 700;
                             font-size: 18px; padding-top: 12px;">
                    ${float(factura.total):,.2f}
                  </td>
                </tr>
              </table>
            </div>

            <p style="color: #888888; font-size: 13px; margin: 0;">
              La factura en PDF está adjunta a este correo.
              Si tienes alguna pregunta, responde a este mensaje.
            </p>
          </div>

          <p style="text-align: center; color: #AAAAAA; font-size: 11px;
                    margin-top: 24px;">
            Nuée Skincare Management · Documento generado electrónicamente
          </p>
        </div>
        """

        msg = Message(
            subject=asunto,
            recipients=[cliente.correo],
            html=cuerpo_html,
            sender=current_app.config.get('MAIL_DEFAULT_SENDER')
        )

        msg.attach(
            filename=f'{factura.numero}.pdf',
            content_type='application/pdf',
            data=pdf_bytes
        )

        mail.send(msg)
        return True, f'Factura enviada a {cliente.correo}'

    except Exception as e:
        current_app.logger.error(f'Error enviando factura {factura.numero}: {e}')
        return False, f'Error al enviar correo: {str(e)}'