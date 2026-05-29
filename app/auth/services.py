import random
from datetime import datetime, timedelta
from app.auth.models import Usuario
from app.extensions import db, mail
from flask_mail import Message

def autenticar_usuario(username, password):
    from sqlalchemy import or_
    usuario = Usuario.query.filter(
        or_(Usuario.username == username, Usuario.email == username),
        Usuario.activo == True
    ).first()
    if usuario and usuario.check_password(password):
        return usuario
    return None

def generar_token_reset(email):
    usuario = Usuario.query.filter_by(email=email, activo=True).first()
    if not usuario:
        return None
    codigo = str(random.randint(100000, 999999))
    usuario.reset_token        = codigo
    usuario.reset_token_expiry = datetime.utcnow() + timedelta(minutes=15)
    db.session.commit()
    return usuario

def resetear_password_con_token(token, nueva_password):
    usuario = Usuario.query.filter_by(reset_token=token).first()
    if not usuario or not usuario.token_valido():
        return False
    usuario.set_password(nueva_password)
    usuario.reset_token        = None
    usuario.reset_token_expiry = None
    db.session.commit()
    return True

def enviar_email_reset(usuario, codigo):
    msg = Message(
        subject    = 'Código de recuperación — Nuée',
        recipients = [usuario.email],
        html       = f"""
        <div style="font-family:Arial,sans-serif;max-width:480px;margin:auto;
                    padding:32px;border-radius:12px;border:1px solid #e5e7eb;">
          <h2 style="color:#2563eb;">🔐 Recuperar contraseña</h2>
          <p>Hola <strong>{usuario.nombre or usuario.username}</strong>,</p>
          <p>Tu código de recuperación es:</p>
          <div style="font-size:2.5rem;font-weight:700;letter-spacing:12px;
                      color:#2563eb;text-align:center;margin:24px 0;">
            {codigo}
          </div>
          <p>Este código expira en <strong>15 minutos</strong>.</p>
          <p style="color:#6b7280;font-size:0.875rem;">
            Si no solicitaste esto, ignora este correo.
          </p>
        </div>
        """
    )
    mail.send(msg)

def resetear_password_admin(usuario_id, nueva_password):
    usuario = Usuario.query.get_or_404(usuario_id)
    usuario.set_password(nueva_password)
    usuario.reset_token        = None
    usuario.reset_token_expiry = None
    db.session.commit()
    return usuario