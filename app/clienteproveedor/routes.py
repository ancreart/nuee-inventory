from flask import render_template, jsonify, request, redirect, url_for, flash
from app.clienteproveedor.forms import ClienteProveedorForm
from app.clienteproveedor.services import (
    listar_clientes,
    buscar_clientes,
    obtener_cliente_por_nit,
    obtener_cliente,
    crear_cliente,
    actualizar_cliente,
    eliminar_cliente
)
from app.clienteproveedor import clienteproveedor_bp


@clienteproveedor_bp.route("/")
def index():
    clientes = listar_clientes()
    form = ClienteProveedorForm()
    return render_template("clienteproveedor/index.html", clientes=clientes, form=form)


@clienteproveedor_bp.route("/crear", methods=["POST"])
def crear():
    form = ClienteProveedorForm()
    if form.validate_on_submit():
        data = {
            'nit':                form.nit.data,
            'nombre':             form.nombre.data,
            'direccion':          form.direccion.data,
            'celular':            form.celular.data,
            'tipo':               form.tipo.data,
            'correo':             form.correo.data,
            'tipo_identificacion':form.tipo_identificacion.data
        }
        try:
            crear_cliente(data)
            flash('Contacto creado exitosamente', 'success')
        except Exception as e:
            flash(f'Error al crear contacto: {str(e)}', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{error}', 'danger')

    return redirect(url_for('clienteproveedor.index'))


@clienteproveedor_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    cliente = obtener_cliente(id)
    if not cliente:
        flash('Cliente no encontrado', 'danger')
        return redirect(url_for('clienteproveedor.index'))

    form = ClienteProveedorForm(obj=cliente)

    if form.validate_on_submit():
        data = {
            'nit':                form.nit.data,
            'nombre':             form.nombre.data,
            'direccion':          form.direccion.data,
            'celular':            form.celular.data,
            'tipo':               form.tipo.data,
            'correo':             form.correo.data,
            'tipo_identificacion':form.tipo_identificacion.data
        }
        try:
            actualizar_cliente(id, data)
            flash('Contacto actualizado exitosamente', 'success')
            return redirect(url_for('clienteproveedor.index'))
        except Exception as e:
            flash(f'Error al actualizar contacto: {str(e)}', 'danger')

    return render_template("clienteproveedor/edit.html", cliente=cliente, form=form)


@clienteproveedor_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    try:
        eliminar_cliente(id)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


# === API ===

@clienteproveedor_bp.route("/api/clientes")
def api_listar_clientes():
    clientes = listar_clientes()
    return jsonify([{
        "id": c.id, "nit": c.nit, "nombre": c.nombre,
        "direccion": c.direccion, "telefono": c.celular, "tipo": c.tipo
    } for c in clientes])


@clienteproveedor_bp.route("/api/clientes/buscar")
def api_buscar_clientes():
    query = request.args.get('q', '')
    clientes = buscar_clientes(query)
    return jsonify([{
        "id": c.id, "nit": c.nit, "nombre": c.nombre,
        "direccion": c.direccion, "telefono": c.celular, "tipo": c.tipo
    } for c in clientes])


@clienteproveedor_bp.route("/api/clientes/nit/<nit>")
def api_cliente_por_nit(nit):
    cliente = obtener_cliente_por_nit(nit)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404
    return jsonify({
        "id": cliente.id, "nit": cliente.nit, "nombre": cliente.nombre,
        "direccion": cliente.direccion, "telefono": cliente.celular, "tipo": cliente.tipo
    })