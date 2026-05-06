from flask import Flask
from app.extensions import db, migrate, mail, csrf
from config import DevelopmentConfig


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    csrf.init_app(app)

    # Blueprints
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

    return app