from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, EmailField
from wtforms.validators import DataRequired, Optional, Length, Email


class ClienteProveedorForm(FlaskForm):

    tipo_identificacion = SelectField(
        'Tipo de Identificación',
        choices=[
            ('NIT', 'NIT'),
            ('CC',  'Cédula de Ciudadanía (CC)'),
            ('CE',  'Cédula de Extranjería (CE)'),
            ('PP',  'Pasaporte (PP)'),
        ],
        default='NIT'
    )

    nit = StringField(
        'Número de Identificación',
        validators=[DataRequired(message='El número de identificación es obligatorio'),
                    Length(max=20)]
    )

    nombre = StringField(
        'Nombre / Razón Social',
        validators=[DataRequired(message='El nombre es obligatorio'),
                    Length(max=150)]
    )

    direccion = StringField(
        'Dirección',
        validators=[Optional(), Length(max=150)]
    )

    celular = StringField(
        'Celular',
        validators=[Optional(), Length(max=20)]
    )

    correo = EmailField(
        'Correo Electrónico',
        validators=[Optional(), Email(message='Ingresa un correo válido'), Length(max=120)]
    )

    tipo = SelectField(
        'Tipo de Contacto',
        choices=[('C', 'Cliente'), ('P', 'Proveedor')],
        default='C'
    )