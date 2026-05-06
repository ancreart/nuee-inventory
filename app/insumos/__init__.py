from flask import Blueprint

##declaramos blueprint

insumos_bp = Blueprint(
    'insumos',
    __name__,
    template_folder = 'templates',
    static_folder= 'static'
)

from .import routes, models