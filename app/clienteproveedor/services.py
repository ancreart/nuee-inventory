from app.extensions import db
from app.clienteproveedor.models import ClienteProveedor


def listar_clientes():
    return ClienteProveedor.query.all()


def buscar_clientes(query):
    if not query:
        return []
    busqueda = f"%{query}%"
    return ClienteProveedor.query.filter(
        db.or_(
            ClienteProveedor.nombre.ilike(busqueda),
            ClienteProveedor.nit.ilike(busqueda)
        )
    ).limit(10).all()


def obtener_cliente(cliente_id):
    return ClienteProveedor.query.get_or_404(cliente_id)


def obtener_cliente_por_nit(nit):
    return ClienteProveedor.query.filter_by(nit=nit).first()


def crear_cliente(data):
    nuevo = ClienteProveedor(
        nit=data.get('nit'),
        nombre=data.get('nombre'),
        direccion=data.get('direccion'),
        celular=data.get('celular'),
        tipo=data.get('tipo', 'C'),
        correo=data.get('correo'),
        tipo_identificacion=data.get('tipo_identificacion', 'NIT')
    )
    db.session.add(nuevo)
    db.session.commit()
    return nuevo


def actualizar_cliente(cliente_id, data):
    cliente = obtener_cliente(cliente_id)
    cliente.nit                 = data.get('nit',                cliente.nit)
    cliente.nombre              = data.get('nombre',             cliente.nombre)
    cliente.direccion           = data.get('direccion',          cliente.direccion)
    cliente.celular             = data.get('celular',            cliente.celular)
    cliente.tipo                = data.get('tipo',               cliente.tipo)
    cliente.correo              = data.get('correo',             cliente.correo)
    cliente.tipo_identificacion = data.get('tipo_identificacion',cliente.tipo_identificacion)
    db.session.commit()
    return cliente


def eliminar_cliente(cliente_id):
    cliente = obtener_cliente(cliente_id)
    db.session.delete(cliente)
    db.session.commit()
    return True