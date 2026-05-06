from flask import Blueprint

facturas_bp = Blueprint('facturas', __name__)

from . import routes