from flask import render_template, redirect, url_for, flash, session, request
from . import auth_bp
from .forms import LoginForm, RegisterForm, PerfilForm
from .services import (
    autenticar_usuario, generar_token_reset,
    enviar_email_reset, resetear_password_con_token,
    resetear_password_admin
)
from .models import Usuario
from app.extensions import db
from sqlalchemy import text
from functools import wraps


# ─── Decoradores centralizados ───────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        if session.get('rol') != 'admin':
            flash('Acceso restringido a administradores', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated


# ─── Autenticación ───────────────────────────────────────────────────────────

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        usuario = autenticar_usuario(form.username.data, form.password.data)
        if usuario:
            session["user_id"]  = usuario.id
            session["username"] = usuario.username
            session["rol"]      = usuario.rol
            if request.form.get("remember"):
                session.permanent = True
            flash("Bienvenido al sistema", "success")
            return redirect(url_for("main.dashboard"))
        flash("Credenciales incorrectas", "danger")
    return render_template("login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))
    form = RegisterForm()
    if form.validate_on_submit():
        if Usuario.query.filter_by(username=form.username.data).first():
            flash("El nombre de usuario ya está en uso", "danger")
            return redirect(url_for("auth.register"))
        if Usuario.query.filter_by(email=form.email.data).first():
            flash("El correo electrónico ya está registrado", "danger")
            return redirect(url_for("auth.register"))
        try:
            nuevo = Usuario(
                username = form.username.data,
                nombre   = form.nombre.data,
                email    = form.email.data,
                rol      = "usuario",
                activo   = True
            )
            nuevo.set_password(form.password.data)
            db.session.add(nuevo)
            db.session.commit()
            flash("Usuario creado. Ahora puedes iniciar sesión", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al crear usuario: {str(e)}", "danger")
            return redirect(url_for("auth.register"))
    return render_template("auth/register.html", form=form)


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión finalizada correctamente", "info")
    return redirect(url_for("auth.login"))


# ─── Recuperación de contraseña ──────────────────────────────────────────────

@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email   = request.form.get("email")
        usuario = generar_token_reset(email)
        if usuario:
            try:
                enviar_email_reset(usuario, usuario.reset_token)
                flash("Código enviado. Revisa tu correo.", "success")
            except Exception as e:
                from flask import current_app
                if current_app.debug:
                    flash(f"⚠️ Modo prueba — código: {usuario.reset_token}", "warning")
                else:
                    flash("Error al enviar el correo. Intenta más tarde.", "danger")
            return redirect(url_for("auth.verify_code", email=email))
        else:
            flash("Si el correo existe, recibirás un código.", "success")
            return redirect(url_for("auth.forgot_password"))
    return render_template("auth/forgot_password.html")


@auth_bp.route("/verify-code", methods=["GET", "POST"])
def verify_code():
    email = request.args.get("email") or request.form.get("email")
    if request.method == "POST":
        codigo  = request.form.get("codigo", "").strip()
        usuario = Usuario.query.filter_by(email=email, reset_token=codigo).first()
        if not usuario or not usuario.token_valido():
            flash("Código inválido o expirado.", "danger")
            return render_template("auth/verify_code.html", email=email)
        return redirect(url_for("auth.reset_password", token=codigo))
    return render_template("auth/verify_code.html", email=email)


@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    usuario = Usuario.query.filter_by(reset_token=token).first()
    if not usuario or not usuario.token_valido():
        flash("El código es inválido o expiró. Solicita uno nuevo.", "danger")
        return redirect(url_for("auth.forgot_password"))
    if request.method == "POST":
        nueva     = request.form.get("password")
        confirmar = request.form.get("confirm_password")
        if nueva != confirmar:
            flash("Las contraseñas no coinciden", "danger")
            return redirect(url_for("auth.reset_password", token=token))
        if len(nueva) < 6:
            flash("La contraseña debe tener al menos 6 caracteres", "danger")
            return redirect(url_for("auth.reset_password", token=token))
        resetear_password_con_token(token, nueva)
        flash("Contraseña actualizada. Ya puedes iniciar sesión.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password.html", token=token)
# ─── Perfil ──────────────────────────────────────────────────────────────────

@auth_bp.route("/perfil", methods=["GET", "POST"])
@login_required
def perfil():
    usuario = Usuario.query.get_or_404(session["user_id"])
    form    = PerfilForm(obj=usuario)
    if form.validate_on_submit():
        if form.email.data != usuario.email:
            if Usuario.query.filter_by(email=form.email.data).first():
                flash("Ese correo ya está registrado por otro usuario", "danger")
                return redirect(url_for("auth.perfil"))
        usuario.nombre = form.nombre.data
        usuario.email  = form.email.data
        if form.password.data:
            usuario.set_password(form.password.data)
        db.session.commit()
        flash("Perfil actualizado correctamente", "success")
        return redirect(url_for("auth.perfil"))
    return render_template("auth/perfil.html", form=form, usuario=usuario)


# ─── Configuración (solo admin) ──────────────────────────────────────────────

@auth_bp.route("/configuracion")
@admin_required
def configuracion():
    usuarios = Usuario.query.order_by(Usuario.id.desc()).all()
    return render_template("auth/configuracion.html", usuarios=usuarios)


@auth_bp.route("/configuracion/usuario/<int:id>/toggle", methods=["POST"])
@admin_required
def toggle_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    if usuario.id == session["user_id"]:
        flash("No puedes desactivarte a ti mismo", "warning")
        return redirect(url_for("auth.configuracion"))
    usuario.activo = not usuario.activo
    db.session.commit()
    estado = "activado" if usuario.activo else "desactivado"
    flash(f"Usuario {usuario.username} {estado}", "success")
    return redirect(url_for("auth.configuracion"))


@auth_bp.route("/configuracion/usuario/<int:id>/rol", methods=["POST"])
@admin_required
def cambiar_rol(id):
    usuario   = Usuario.query.get_or_404(id)
    if usuario.id == session["user_id"]:
        flash("No puedes cambiar tu propio rol", "warning")
        return redirect(url_for("auth.configuracion"))
    nuevo_rol = request.form.get("rol")
    if nuevo_rol in ["admin", "usuario"]:
        usuario.rol = nuevo_rol
        db.session.commit()
        flash(f"Rol de {usuario.username} cambiado a {nuevo_rol}", "success")
    return redirect(url_for("auth.configuracion"))

@auth_bp.route("/configuracion/nuevo-usuario", methods=["GET", "POST"])
@admin_required
def admin_crear_usuario():
    form = RegisterForm()
    if form.validate_on_submit():
        if Usuario.query.filter_by(username=form.username.data).first():
            flash("El nombre de usuario ya está en uso", "danger")
            return redirect(url_for("auth.admin_crear_usuario"))
        if Usuario.query.filter_by(email=form.email.data).first():
            flash("El correo electrónico ya está registrado", "danger")
            return redirect(url_for("auth.admin_crear_usuario"))
        try:
            nuevo = Usuario(
                username = form.username.data,
                nombre   = form.nombre.data,
                email    = form.email.data,
                rol      = "usuario",
                activo   = True
            )
            nuevo.set_password(form.password.data)
            db.session.add(nuevo)
            db.session.commit()
            flash(f"Usuario '{form.username.data}' creado correctamente", "success")
            return redirect(url_for("auth.configuracion"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al crear usuario: {str(e)}", "danger")
            return redirect(url_for("auth.admin_crear_usuario"))
    return render_template("auth/admin_crear_usuario.html", form=form)

# ─── Admin usuarios (legacy, sigue funcionando) ──────────────────────────────

@auth_bp.route("/admin/usuarios")
@admin_required
def admin_usuarios():
    usuarios = Usuario.query.order_by(Usuario.id.desc()).all()
    return render_template("auth/admin_usuarios.html", usuarios=usuarios)


@auth_bp.route("/admin/usuarios/<int:id>/reset", methods=["POST"])
@admin_required
def admin_reset_password(id):
    import secrets
    nueva = secrets.token_urlsafe(8)
    resetear_password_admin(id, nueva)
    flash(f"Contraseña reseteada. Nueva contraseña temporal: {nueva}", "success")
    return redirect(url_for("auth.admin_usuarios"))


# ─── Test DB ─────────────────────────────────────────────────────────────────

@auth_bp.route("/test-db")
def test_db():
    result = db.session.execute(text("SELECT DB_NAME()")).scalar()
    return f"Base conectada: {result}"