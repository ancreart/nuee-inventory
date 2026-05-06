from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField, IntegerField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, InputRequired


class InsumoForm(FlaskForm):
    codigo = StringField(
        'Código',
        validators=[
            DataRequired(message="El código es obligatorio"),
            Length(max=15)
        ]
    )

    descripcion = StringField(
        'Descripción',
        validators=[
            DataRequired(message="La descripción es obligatoria"),
            Length(max=150)
        ]
    )

    lote = StringField(
        'Lote',
        validators=[
            DataRequired(message="El lote es obligatorio"),
            Length(max=12)
        ]
    )

    invima = StringField(
        'Registro INVIMA',
        validators=[
            Optional(),
            Length(max=15)
        ]
    )

    valor = DecimalField(
        'Valor',
        validators=[
            DataRequired(message="El valor es obligatorio"),
            NumberRange(min=0)
        ],
        places=2
    )

    iva = DecimalField(
        'IVA %',
        validators=[
            Optional(),
            NumberRange(min=0, max=100)
        ],
        places=2,
        default=0
    )

    cantidad = IntegerField(
        'Cantidad',
        validators=[
            InputRequired(message="La cantidad es obligatoria"),
            NumberRange(min=0, message="La cantidad no puede ser negativa")
        ],
        default=0
    )

    stock_minimo = IntegerField(
        'Stock Mínimo',
        validators=[
            InputRequired(message="El stock mínimo es obligatorio"),
            NumberRange(min=0, message="El stock mínimo no puede ser negativo")
        ],
        default=5
    )

    fecha_vencimiento = DateField(
        'Fecha de Vencimiento',
        validators=[Optional()],
        format='%Y-%m-%d'
    )

    activo = BooleanField('Activo', default=True)

    submit = SubmitField('Guardar')