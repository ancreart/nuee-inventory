from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional


class FacturaForm(FlaskForm):
    id_cliente = IntegerField(
        "Cliente",
        validators=[DataRequired(message="Seleccione un cliente")]
    )
    observaciones = TextAreaField(
        "Observaciones",
        validators=[Optional()]
    )
    submit = SubmitField("Crear Factura")