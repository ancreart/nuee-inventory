from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional


class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit   = SubmitField("Ingresar")


class RegisterForm(FlaskForm):
    nombre           = StringField("Nombre completo",
                                   validators=[DataRequired(), Length(max=100)])
    email            = EmailField("Correo electrónico",
                                  validators=[DataRequired(), Email()])
    username         = StringField("Nombre de usuario",
                                   validators=[DataRequired(), Length(min=3, max=50)])
    password         = PasswordField("Contraseña",
                                     validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirmar contraseña",
                                     validators=[DataRequired(),
                                                 EqualTo("password",
                                                         message="Las contraseñas no coinciden")])
    submit           = SubmitField("Crear usuario")


class PerfilForm(FlaskForm):
    nombre   = StringField("Nombre completo",
                           validators=[DataRequired(), Length(max=100)])
    email    = EmailField("Correo electrónico",
                          validators=[DataRequired(), Email()])
    password = PasswordField("Nueva contraseña (opcional)",
                             validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField("Confirmar nueva contraseña",
                                     validators=[Optional(),
                                                 EqualTo("password",
                                                         message="Las contraseñas no coinciden")])
    submit   = SubmitField("Guardar cambios")