from flask import Blueprint

# declaramos blueprint
clienteproveedor_bp = Blueprint(
    'clienteproveedor',
    __name__,
    template_folder='templates',
    static_folder='static'
)

from . import routes, models