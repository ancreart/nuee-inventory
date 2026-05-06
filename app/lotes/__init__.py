from flask import Blueprint

lotes_bp = Blueprint('lotes', __name__)

from . import routes