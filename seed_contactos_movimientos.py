"""
seed_contactos_movimientos.py
Pobla clientes, proveedores y movimientos de la última semana.
Ejecutar desde la raíz del proyecto: python seed_contactos_movimientos.py
"""

from app import create_app
from app.extensions import db
from app.clienteproveedor.models import ClienteProveedor
from app.movimientos.models import Movimiento
from app.insumos.models import Insumo
from datetime import datetime, timedelta, date
import random

app = create_app()

# ── CLIENTES (25) ─────────────────────────────────────────────────────────────
CLIENTES = [
    {"nit": "52.801.234-1", "nombre": "Valentina Ríos Martínez",       "direccion": "Cra 15 #93-47, Bogotá",          "celular": "3101234567", "correo": "vrios@gmail.com",          "tipo_id": "CC"},
    {"nit": "43.612.890-2", "nombre": "Camila Ospina Herrera",          "direccion": "Cl 10 #43-25, Medellín",         "celular": "3202345678", "correo": "cospina@gmail.com",         "tipo_id": "CC"},
    {"nit": "30.412.567-3", "nombre": "Mariana Gómez Restrepo",         "direccion": "Av 6N #23-15, Cali",             "celular": "3153456789", "correo": "mgomez@hotmail.com",        "tipo_id": "CC"},
    {"nit": "46.901.123-4", "nombre": "Daniela Vargas Suárez",          "direccion": "Cra 27 #57-12, Bucaramanga",     "celular": "3004567890", "correo": "dvargas@gmail.com",         "tipo_id": "CC"},
    {"nit": "32.711.456-5", "nombre": "Sofía Mendoza Peña",             "direccion": "Cl 72 #68-30, Barranquilla",     "celular": "3185678901", "correo": "smendoza@outlook.com",      "tipo_id": "CC"},
    {"nit": "51.234.789-6", "nombre": "Isabella Castro Mora",           "direccion": "Cra 11 #82-44, Bogotá",          "celular": "3106789012", "correo": "icastro@gmail.com",         "tipo_id": "CC"},
    {"nit": "42.567.890-7", "nombre": "Luciana Fernández Álvarez",      "direccion": "Cl 33 #76-20, Medellín",         "celular": "3207890123", "correo": "lfernandez@gmail.com",      "tipo_id": "CC"},
    {"nit": "29.345.678-8", "nombre": "Natalia Jiménez Torres",         "direccion": "Av 3N #12-08, Cali",             "celular": "3158901234", "correo": "njimenez@hotmail.com",      "tipo_id": "CC"},
    {"nit": "47.890.123-9", "nombre": "Alejandra Ruiz Pinto",           "direccion": "Cra 33 #48-60, Bucaramanga",     "celular": "3009012345", "correo": "aruiz@gmail.com",           "tipo_id": "CC"},
    {"nit": "33.456.789-0", "nombre": "Gabriela Moreno Díaz",           "direccion": "Cl 84 #45-17, Barranquilla",     "celular": "3190123456", "correo": "gmoreno@gmail.com",         "tipo_id": "CC"},
    {"nit": "53.012.345-1", "nombre": "Paulina Salcedo Gómez",          "direccion": "Cra 7 #116-50, Bogotá",          "celular": "3101234568", "correo": "psalcedo@gmail.com",        "tipo_id": "CC"},
    {"nit": "44.678.901-2", "nombre": "Manuela Agudelo Ríos",           "direccion": "Cl 50 #52-36, Medellín",         "celular": "3202345679", "correo": "magudelo@outlook.com",      "tipo_id": "CC"},
    {"nit": "31.234.567-3", "nombre": "Catalina Prada Londoño",         "direccion": "Av 5N #34-22, Cali",             "celular": "3153456780", "correo": "cprada@gmail.com",          "tipo_id": "CC"},
    {"nit": "48.567.890-4", "nombre": "Verónica Pedraza Niño",          "direccion": "Cra 22 #35-14, Bucaramanga",     "celular": "3004567891", "correo": "vpedraza@gmail.com",        "tipo_id": "CC"},
    {"nit": "34.890.123-5", "nombre": "Juliana Ramos Espinosa",         "direccion": "Cl 53 #38-29, Barranquilla",     "celular": "3185678902", "correo": "jramos@gmail.com",          "tipo_id": "CC"},
    {"nit": "54.345.678-6", "nombre": "Andrea Muñoz Cardona",           "direccion": "Cra 9 #72-18, Bogotá",           "celular": "3106789013", "correo": "amunoz@hotmail.com",        "tipo_id": "CC"},
    {"nit": "45.901.234-7", "nombre": "Valeria Quintero Betancur",      "direccion": "Cl 37 #65-41, Medellín",         "celular": "3207890124", "correo": "vquintero@gmail.com",       "tipo_id": "CC"},
    {"nit": "28.456.789-8", "nombre": "Simona Arango Vélez",            "direccion": "Av 8N #19-33, Cali",             "celular": "3158901235", "correo": "sarango@gmail.com",         "tipo_id": "CC"},
    {"nit": "49.012.345-9", "nombre": "Renata Serrano Blanco",          "direccion": "Cra 28 #42-55, Bucaramanga",     "celular": "3009012346", "correo": "rserrano@outlook.com",      "tipo_id": "CC"},
    {"nit": "35.567.890-0", "nombre": "Emilia Cárdenas Fuentes",        "direccion": "Cl 79 #41-26, Barranquilla",     "celular": "3190123457", "correo": "ecardenas@gmail.com",       "tipo_id": "CC"},
    {"nit": "55.123.456-1", "nombre": "Antonella Herrera Acosta",       "direccion": "Cra 13 #85-32, Bogotá",          "celular": "3101234569", "correo": "aherrera@gmail.com",        "tipo_id": "CC"},
    {"nit": "41.789.012-2", "nombre": "Luna Zapata Gutiérrez",          "direccion": "Cl 44 #80-15, Medellín",         "celular": "3202345670", "correo": "lzapata@gmail.com",         "tipo_id": "CC"},
    {"nit": "27.345.678-3", "nombre": "Sara Castaño Mejía",             "direccion": "Av 4N #27-19, Cali",             "celular": "3153456781", "correo": "scastano@hotmail.com",      "tipo_id": "CC"},
    {"nit": "36.901.234-4", "nombre": "Alicia Bermúdez Ochoa",          "direccion": "Cra 35 #55-38, Bucaramanga",     "celular": "3004567892", "correo": "abermudez@gmail.com",       "tipo_id": "CC"},
    {"nit": "56.678.901-5", "nombre": "Regina Molina Cifuentes",        "direccion": "Cl 48 #32-47, Barranquilla",     "celular": "3185678903", "correo": "rmolina@gmail.com",         "tipo_id": "CC"},
]

# ── PROVEEDORES (25) ──────────────────────────────────────────────────────────
PROVEEDORES = [
    {"nit": "900.123.456-1", "nombre": "Belleza & Cosmética S.A.S",          "direccion": "Cra 68 #22-31, Bogotá",          "celular": "6017234567", "correo": "ventas@bellezacosmetica.co",     "tipo_id": "NIT"},
    {"nit": "900.234.567-2", "nombre": "Distribuciones Derma Colombia",       "direccion": "Cl 80 #45-12, Medellín",         "celular": "6044512890", "correo": "pedidos@dermacolombia.co",       "tipo_id": "NIT"},
    {"nit": "900.345.678-3", "nombre": "Importadora Skin Care Andina",        "direccion": "Av 6N #14-55, Cali",             "celular": "6022398741", "correo": "contacto@skinandina.com",        "tipo_id": "NIT"},
    {"nit": "900.456.789-4", "nombre": "Laboratorios Natura Vital Ltda",      "direccion": "Cra 15 #63-20, Bucaramanga",     "celular": "6076341209", "correo": "lab@naturavital.co",             "tipo_id": "NIT"},
    {"nit": "900.567.890-5", "nombre": "Cosméticos del Caribe S.A",           "direccion": "Cl 72 #43-18, Barranquilla",     "celular": "6053287654", "correo": "info@cosmeticoscaribe.com",      "tipo_id": "NIT"},
    {"nit": "900.678.901-6", "nombre": "Global Beauty Solutions Colombia",     "direccion": "Cra 7 #127-60, Bogotá",          "celular": "6017890123", "correo": "ventas@globalbeauty.co",         "tipo_id": "NIT"},
    {"nit": "900.789.012-7", "nombre": "Dermocosméticos Antioquia S.A.S",     "direccion": "Cl 10 #38-44, Medellín",         "celular": "6044678234", "correo": "contacto@dermoantioquia.co",     "tipo_id": "NIT"},
    {"nit": "900.890.123-8", "nombre": "Proveedora Nacional de Skincare",      "direccion": "Av 3N #28-19, Cali",             "celular": "6022156789", "correo": "pedidos@skincarenacional.co",    "tipo_id": "NIT"},
    {"nit": "900.901.234-9", "nombre": "Industrias Cosméticas del Sur",        "direccion": "Cra 40 #52-35, Bucaramanga",     "celular": "6076512345", "correo": "ventas@cosmeticosdelsur.co",     "tipo_id": "NIT"},
    {"nit": "901.012.345-0", "nombre": "Biocosmética Premium Colombia",        "direccion": "Cl 53 #31-27, Barranquilla",     "celular": "6053190876", "correo": "info@biocosmetica.co",           "tipo_id": "NIT"},
    {"nit": "901.123.456-1", "nombre": "Peptide Lab Distribuciones",           "direccion": "Cra 11 #90-14, Bogotá",          "celular": "6017345678", "correo": "lab@peptidelab.co",              "tipo_id": "NIT"},
    {"nit": "901.234.567-2", "nombre": "Ceramide & Co Importaciones",          "direccion": "Cl 45 #70-22, Medellín",         "celular": "6044234567", "correo": "imports@ceramideco.com",         "tipo_id": "NIT"},
    {"nit": "901.345.678-3", "nombre": "Dermaline Colombia S.A.S",             "direccion": "Av 5N #40-33, Cali",             "celular": "6022789012", "correo": "ventas@dermalineco.co",          "tipo_id": "NIT"},
    {"nit": "901.456.789-4", "nombre": "Wellness Cosmetics Distribuidora",     "direccion": "Cra 30 #48-17, Bucaramanga",     "celular": "6076234890", "correo": "contacto@wellnessco.co",         "tipo_id": "NIT"},
    {"nit": "901.567.890-5", "nombre": "Atlántico Beauty Mayorista",           "direccion": "Cl 84 #52-41, Barranquilla",     "celular": "6053456123", "correo": "mayorista@atlanticobeauty.co",   "tipo_id": "NIT"},
    {"nit": "901.678.901-6", "nombre": "Skinlab Bogotá Proveedores",           "direccion": "Cra 9 #65-28, Bogotá",           "celular": "6017456789", "correo": "lab@skinlabbogota.co",           "tipo_id": "NIT"},
    {"nit": "901.789.012-7", "nombre": "Medellín Glow Distribuciones",         "direccion": "Cl 30 #80-55, Medellín",         "celular": "6044890123", "correo": "glow@medellinglow.co",           "tipo_id": "NIT"},
    {"nit": "901.890.123-8", "nombre": "Valle Cosmético S.A",                  "direccion": "Av 9N #15-44, Cali",             "celular": "6022345678", "correo": "ventas@vallecosmetico.co",       "tipo_id": "NIT"},
    {"nit": "901.901.234-9", "nombre": "Provitalia Skincare Colombia",          "direccion": "Cra 25 #60-39, Bucaramanga",     "celular": "6076789234", "correo": "info@provitalia.co",             "tipo_id": "NIT"},
    {"nit": "902.012.345-0", "nombre": "Cosmética Sostenible del Norte",        "direccion": "Cl 63 #38-26, Barranquilla",     "celular": "6053678901", "correo": "eco@cosmeticanorte.co",          "tipo_id": "NIT"},
    {"nit": "902.123.456-1", "nombre": "Glaze Import Export S.A.S",            "direccion": "Cra 13 #100-17, Bogotá",         "celular": "6017567890", "correo": "imports@glazeco.com",            "tipo_id": "NIT"},
    {"nit": "902.234.567-2", "nombre": "Antioquia Dermis Laboratorio",          "direccion": "Cl 55 #62-14, Medellín",         "celular": "6044123456", "correo": "lab@antioquiadermis.co",         "tipo_id": "NIT"},
    {"nit": "902.345.678-3", "nombre": "Pacific Skin Distribuciones",           "direccion": "Av 2N #50-21, Cali",             "celular": "6022901234", "correo": "ventas@pacificskin.co",          "tipo_id": "NIT"},
    {"nit": "902.456.789-4", "nombre": "Santander Beauty Mayorista",            "direccion": "Cra 18 #72-43, Bucaramanga",     "celular": "6076345678", "correo": "mayorista@santanderbeauty.co",   "tipo_id": "NIT"},
    {"nit": "902.567.890-5", "nombre": "Caribe Glow Importaciones Ltda",        "direccion": "Cl 45 #27-38, Barranquilla",     "celular": "6053234567", "correo": "imports@caribeglow.co",          "tipo_id": "NIT"},
]


def seed_contactos():
    """Inserta clientes y proveedores si la tabla está vacía."""
    existentes = ClienteProveedor.query.count()
    if existentes > 0:
        print(f"  ⚠️  Ya existen {existentes} contactos. Omitiendo clientes/proveedores.")
        return

    for c in CLIENTES:
        registro = ClienteProveedor(
            nit                 = c["nit"],
            nombre              = c["nombre"],
            direccion           = c["direccion"],
            celular             = c["celular"],
            correo              = c["correo"],
            tipo                = "Cliente",
            tipo_identificacion = c["tipo_id"],
        )
        db.session.add(registro)

    for p in PROVEEDORES:
        registro = ClienteProveedor(
            nit                 = p["nit"],
            nombre              = p["nombre"],
            direccion           = p["direccion"],
            celular             = p["celular"],
            correo              = p["correo"],
            tipo                = "Proveedor",
            tipo_identificacion = p["tipo_id"],
        )
        db.session.add(registro)

    db.session.commit()
    print(f"  ✓ 25 clientes insertados")
    print(f"  ✓ 25 proveedores insertados")


def seed_movimientos():
    """
    Genera movimientos de los últimos 7 días.
    - Salidas (ventas): vinculadas a clientes, reflejan demanda real
    - Entradas (reposición): vinculadas a proveedores
    Los productos más vendidos son labiales y esencias — productos de ticket
    rápido en el mercado colombiano de skincare.
    """
    existentes = Movimiento.query.count()
    if existentes > 0:
        print(f"  ⚠️  Ya existen {existentes} movimientos. Omitiendo movimientos.")
        return

    insumos = Insumo.query.filter_by(activo=True).all()
    if not insumos:
        print("  ✗ No hay insumos en la base de datos. Corre seed_nuee.py primero.")
        return

    clientes   = ClienteProveedor.query.filter_by(tipo="Cliente").all()
    proveedores = ClienteProveedor.query.filter_by(tipo="Proveedor").all()

    if not clientes or not proveedores:
        print("  ✗ No hay clientes/proveedores. Algo falló en seed_contactos().")
        return

    hoy = datetime.utcnow()

    # Pesos de venta por producto — los labiales y esencias rotan más rápido
    pesos_venta = {
        "NUE-001": 18,   # Esencia Ceramida — hero product
        "NUE-002": 22,   # Tinte Labial — mayor rotación
        "NUE-003": 10,
        "NUE-004": 12,
        "NUE-005": 10,
        "NUE-006": 20,   # Mascarilla Labial — alta rotación
        "NUE-007": 14,
        "NUE-008": 9,
        "NUE-009": 18,   # Tratamiento Labial
        "NUE-010": 11,
        "NUE-011": 13,
        "NUE-012": 12,
        "NUE-013": 15,   # Mini Esencia — impulso por precio
        "NUE-014": 13,
        "NUE-015": 14,
        "NUE-016": 8,    # Kit — menor frecuencia, mayor ticket
        "NUE-017": 12,
        "NUE-018": 11,
    }

    insumo_map = {ins.codigo: ins for ins in insumos}
    codigos    = list(pesos_venta.keys())
    pesos      = [pesos_venta[c] for c in codigos]

    movimientos_generados = 0

    # ── Salidas (ventas) — 6 a 10 por día durante 7 días ──
    for dias_atras in range(7):
        fecha_dia = hoy - timedelta(days=dias_atras)
        ventas_del_dia = random.randint(6, 10)

        for _ in range(ventas_del_dia):
            codigo_elegido = random.choices(codigos, weights=pesos, k=1)[0]
            insumo = insumo_map.get(codigo_elegido)
            if not insumo:
                continue

            cliente = random.choice(clientes)
            cantidad = random.randint(1, 3)

            # Hora aleatoria dentro del día (9am - 7pm)
            hora = random.randint(9, 19)
            minuto = random.randint(0, 59)
            fecha_mov = fecha_dia.replace(hour=hora, minute=minuto, second=0, microsecond=0)

            mov = Movimiento(
                id_cliente     = cliente.id,
                id_insumo      = insumo.id,
                id_usuario     = 1,
                nombre_usuario = "admin",
                tipo           = "salida",
                precio         = float(insumo.valor),
                cantidad       = cantidad,
                fecha_creacion = fecha_mov,
                observaciones  = "Venta mostrador",
                fecha_vencimiento = insumo.fecha_vencimiento,
            )
            db.session.add(mov)
            movimientos_generados += 1

    # ── Entradas (reposición de inventario) — 2 a 3 por día ──
    for dias_atras in range(7):
        fecha_dia = hoy - timedelta(days=dias_atras)
        entradas_del_dia = random.randint(2, 3)

        for _ in range(entradas_del_dia):
            insumo = random.choice(insumos)
            proveedor = random.choice(proveedores)
            cantidad = random.randint(10, 30)

            hora = random.randint(8, 12)
            minuto = random.randint(0, 59)
            fecha_mov = fecha_dia.replace(hour=hora, minute=minuto, second=0, microsecond=0)

            # Costo de entrada es aprox 57% del precio de venta (inverso del margen 75%)
            costo_entrada = round(float(insumo.valor) / 1.75, 2)

            mov = Movimiento(
                id_cliente     = proveedor.id,
                id_insumo      = insumo.id,
                id_usuario     = 1,
                nombre_usuario = "admin",
                tipo           = "entrada",
                precio         = costo_entrada,
                cantidad       = cantidad,
                fecha_creacion = fecha_mov,
                observaciones  = "Reposición de inventario",
                fecha_vencimiento = insumo.fecha_vencimiento,
            )
            db.session.add(mov)
            movimientos_generados += 1

    db.session.commit()
    print(f"  ✓ {movimientos_generados} movimientos generados (últimos 7 días)")


def seed():
    with app.app_context():
        print("\nNuée — Seed de contactos y movimientos")
        print("─" * 45)

        print("\n[1/2] Clientes y proveedores...")
        seed_contactos()

        print("\n[2/2] Movimientos de la última semana...")
        seed_movimientos()

        print("\n✅ Seed completado.")
        print("   El dashboard ahora mostrará estadísticas y top productos.\n")


if __name__ == "__main__":
    seed()