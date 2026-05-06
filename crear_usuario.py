# crear_usuario.py
from app import create_app
from app.extensions import db
from app.auth.models import Usuario

app = create_app()

with app.app_context():
    # Verifica si el usuario ya existe
    existe = Usuario.query.filter_by(username="ana").first()
    
    if not existe:
        usuario = Usuario(
            username="byanmm",
            nombre="Ana Melo",
            rol="admin",
            activo=True
        )
        usuario.set_password("1234")  # Contraseña: 123456
        db.session.add(usuario)
        db.session.commit()
        print("✅ Usuario 'byanmm' creado con éxito")
        print("   Usuario: byanmm")
        print("   Contraseña: 1234")
    else:
        print("ℹ️ El usuario 'byanmm' ya existe en la base de datos")