from flask import Flask, request, session, Blueprint, redirect
from app.extensions import db, migrate, mail, csrf, babel
from config import DevelopmentConfig


def get_locale():
    """Detecta idioma desde sesión, luego navegador, luego español por defecto."""
    if 'lang' in session:
        return session['lang']
    from flask import current_app
    return request.accept_languages.best_match(
        current_app.config.get('LANGUAGES', ['es']), default='es'
    )


lang_bp = Blueprint('lang', __name__)

@lang_bp.route('/lang/<codigo>')
def cambiar_idioma(codigo):
    from flask import current_app
    if codigo in current_app.config.get('LANGUAGES', []):
        session.permanent = True
        session['lang'] = codigo
    return redirect(request.referrer or '/')


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    csrf.init_app(app)
    babel.init_app(app, locale_selector=get_locale)

    @app.context_processor
    def inject_locale():
        return dict(get_locale=get_locale)

    from app.insumos import insumos_bp
    app.register_blueprint(insumos_bp, url_prefix='/insumos')

    from app.clienteproveedor import clienteproveedor_bp
    app.register_blueprint(clienteproveedor_bp, url_prefix='/clienteproveedor')

    from app.movimientos import movimientos_bp
    app.register_blueprint(movimientos_bp, url_prefix='/movimientos')

    from app.main import main_bp
    app.register_blueprint(main_bp)

    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.facturas import facturas_bp
    app.register_blueprint(facturas_bp, url_prefix='/facturas')

    from app.lotes import lotes_bp
    app.register_blueprint(lotes_bp, url_prefix='/lotes')

    app.register_blueprint(lang_bp)

    return app