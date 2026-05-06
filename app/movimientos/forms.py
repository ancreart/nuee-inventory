from flask_wtf import FlaskForm
from wtforms import (IntegerField, DecimalField, SelectField,
                     TextAreaField, DateField, StringField, SubmitField)
from wtforms.validators import DataRequired, NumberRange, Optional


class MovimientoForm(FlaskForm):
    id_cliente = IntegerField(
        "Cliente",
        validators=[DataRequired(message="Seleccione un cliente")]
    )
    id_insumo = IntegerField(
        "Insumo",
        validators=[DataRequired(message="Seleccione un insumo")]
    )
    tipo = SelectField(
        "Tipo de operación",
        choices=[
            ("salida",    "Venta (Salida)"),
            ("entrada",   "Compra (Entrada)"),
            ("devolucion","Devolución")
        ],
        validators=[DataRequired()]
    )
    precio = DecimalField(
        "Precio unitario",
        validators=[DataRequired(), NumberRange(min=0)],
        places=2
    )
    cantidad = IntegerField(
        "Cantidad",
        validators=[DataRequired(), NumberRange(min=1)],
        default=1
    )
    numero = StringField(
        "N° Comprobante",
        validators=[Optional()]
    )
    fecha_vencimiento = DateField(
        "Vencimiento del lote",
        validators=[Optional()],
        format="%Y-%m-%d"
    )
    observaciones = TextAreaField(
        "Observaciones",
        validators=[Optional()]
    )
    submit = SubmitField("Guardar Movimiento")