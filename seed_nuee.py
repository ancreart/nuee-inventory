"""
seed_nuee.py
Pobla la base de datos de Nuée con el catálogo inicial de productos.
Ejecutar desde la raíz del proyecto: python seed_nuee.py
"""

from app import create_app
from app.extensions import db
from app.insumos.models import Insumo
from datetime import date

app = create_app()

# Catálogo Nuée — inspirado en Rhode Skin, adaptado para el mercado colombiano
# Precios en COP. Costo estimado × 1.75 = precio de venta.
# IVA 19% sobre cosméticos (Estatuto Tributario Colombia, art. 468-1).
# Fecha de vencimiento: 2 años desde hoy (estándar cosmético).
# Stock inicial: 100 unidades. Registrado por: admin.

PRODUCTOS = [
    {
        "codigo":            "NUE-001",
        "descripcion":       "Esencia Facial de Ceramida Glazing Milk",
        "lote":              "LT-NUE-001A",
        "invima":            "INV-2024-0001",
        "costo":             85000,
        "iva":               19.00,
        "fecha_vencimiento": date(2027, 6, 1),
    },
    {
        "codigo":            "NUE-002",
        "descripcion":       "Tinte Labial Nutritivo con Péptidos Peptide Lip",
        "lote":              "LT-NUE-002A",
        "invima":            "INV-2024-0002",
        "costo":             52000,
        "iva":               19.00,
        "fecha_vencimiento": date(2027, 6, 1),
    },
    {
        "codigo":            "NUE-003",
        "descripcion":       "Parches Oculares Descongestionantes con Péptidos",
        "lote":              "LT-NUE-003A",
        "invima":            "INV-2024-0003",
        "costo":             68000,
        "iva":               19.00,
        "fecha_vencimiento": date(2027, 6, 1),
    },
    {
        "codigo":            "NUE-004",
        "descripcion":       "Spray Facial Hidratante Glazing Mist",
        "lote":              "LT-NUE-004A",
        "invima":            "INV-2024-0004",
        "costo":             72000,
        "iva":               19.00,
        "fecha_vencimiento": date(2027, 6, 1),
    },
    {
        "codigo":            "NUE-005",
        "descripcion":       "Bruma Hidratante Facial Softening Mist",
        "lote":              "LT-NUE-005A",
        "invima":            "INV-2024-0005",
        "costo":             65000,
        "iva":               19.00,
        "fecha_vencimiento": date(2027, 6, 1),
    },
    {
        "codigo":            "NUE-006",
        "descripcion":       "Mascarilla Labial Voluminizadora con Péptidos Peptide Lip Shape",
        "lote":              "LT-NUE-006A",
        "invima":            "INV-2024-0006",
        "costo":             48000,
        "iva":               19.00,
        "fecha_vencimiento": date(2027, 6, 1),
    },
    {
        "codigo":            "NUE-007",
        "descripcion":       "Bálsamo Hidratante Intensivo Barrier Butter",
        "lote":              "LT-NUE-007A",
        "invima":            "INV-2024-0007",
        "costo":             78000,
        "iva":               19.00,
        "fecha_vencimiento": date(2027, 6, 1),
    },
    {
        "codigo":            "NUE-008",
        "descripcion":       "Mascarilla en Crema Reafirmante con Cafeína Peptide Glazing Mask",
        "lote":              "LT-NUE-008A",
        "invima":            "INV-2024-0008",
        "costo":             92000,
        "iva":               19.00,
        "fecha_vencimiento": date(2027, 6, 1),
    },
    {
        "codigo":            "NUE-009",
        "descripcion":       "Tratamiento Labial Nutritivo Intensive Peptide Lip Treatment",
        "lote":              "LT-NUE-009A",
        "invima":            "INV-2024-0009",
        "costo":             44000,
        "iva":               19.00,
        "fecha_vencimiento": date(2027, 6, 1),
    },
    {
        "codigo":            "NUE-010",
        "descripcion":       "Crema Reparadora de Barrera Barrier Restore Cream",
        "lote":              "LT-NUE-010A",
        "invima":            "INV-2024-0010",
        "costo":             98000,
        "iva":               19.00,
        "fecha_vencimiento": date(2027, 6, 1),
    },
    {
        "codigo":            "NUE-011",
        "descripcion":       "Fluido de Péptidos con Efecto Glaseado Peptide Glazing Fluid",
        "lote":              "LT-NUE-011A",
        "invima":            "INV-2024-0011",
        "costo":             88000,
        "iva":               19.00,
        "fecha_vencimiento": date(2027, 6, 1),
    },
    {
        "codigo":            "NUE-012",
        "descripcion":       "Limpiador Facial Diario Pineapple Refresh PGA Cleanser",
        "lote":              "LT-NUE-012A",
        "invima":            "INV-2024-0012",
        "costo":             62000,
        "iva":               19.00,
        "fecha_vencimiento": date(2027, 6, 1),
    },
    {
        "codigo":            "NUE-013",
        "descripcion":       "Mini Esencia Facial de Ceramida Glazing Milk",
        "lote":              "LT-NUE-013A",
        "invima":            "INV-2024-0013",
        "costo":             38000,
        "iva":               19.00,
        "fecha_vencimiento": date(2027, 6, 1),
    },
    {
        "codigo":            "NUE-014",
        "descripcion":       "Mini Limpiador Facial Pineapple Refresh PGA",
        "lote":              "LT-NUE-014A",
        "invima":            "INV-2024-0014",
        "costo":             32000,
        "iva":               19.00,
        "fecha_vencimiento": date(2027, 6, 1),
    },
    {
        "codigo":            "NUE-015",
        "descripcion":       "Mini Bálsamo Hidratante Barrier Butter",
        "lote":              "LT-NUE-015A",
        "invima":            "INV-2024-0015",
        "costo":             35000,
        "iva":               19.00,
        "fecha_vencimiento": date(2027, 6, 1),
    },
    {
        "codigo":            "NUE-016",
        "descripcion":       "Mini Kit Nuée Esenciales de Skincare",
        "lote":              "LT-NUE-016A",
        "invima":            "INV-2024-0016",
        "costo":             115000,
        "iva":               19.00,
        "fecha_vencimiento": date(2027, 6, 1),
    },
    {
        "codigo":            "NUE-017",
        "descripcion":       "Mini Fluido de Péptidos Glazing Dewy Gel Serum",
        "lote":              "LT-NUE-017A",
        "invima":            "INV-2024-0017",
        "costo":             42000,
        "iva":               19.00,
        "fecha_vencimiento": date(2027, 6, 1),
    },
    {
        "codigo":            "NUE-018",
        "descripcion":       "Mini Crema Reparadora de Barrera Barrier Restore Cream",
        "lote":              "LT-NUE-018A",
        "invima":            "INV-2024-0018",
        "costo":             45000,
        "iva":               19.00,
        "fecha_vencimiento": date(2027, 6, 1),
    },
]


def calcular_precio_venta(costo: int) -> float:
    """Aplica margen del 75% sobre el costo base."""
    return round(costo * 1.75, 2)


def seed():
    with app.app_context():

        # Verificar que no haya insumos antes de insertar
        existentes = Insumo.query.count()
        if existentes > 0:
            print(f"⚠️  Ya existen {existentes} insumos en la base de datos.")
            print("   Ejecuta primero el script SQL de limpieza y vuelve a correr este seed.")
            return

        print("Insertando catálogo Nuée...\n")

        for p in PRODUCTOS:
            precio_venta = calcular_precio_venta(p["costo"])

            insumo = Insumo(
                codigo            = p["codigo"],
                descripcion       = p["descripcion"],
                lote              = p["lote"],
                invima            = p["invima"],
                valor             = precio_venta,
                iva               = p["iva"],
                cantidad          = 100,
                stock_minimo      = 5,
                fecha_vencimiento = p["fecha_vencimiento"],
                activo            = True,
                creado_por        = "admin",
            )
            db.session.add(insumo)
            print(f"  ✓ {p['codigo']} — {p['descripcion'][:50]}")
            print(f"       Costo: ${p['costo']:,}  →  Venta: ${precio_venta:,.2f}  |  IVA: {p['iva']}%")

        db.session.commit()
        print(f"\n✅ {len(PRODUCTOS)} productos insertados correctamente.")
        print("   Stock: 100 uds. por producto | IVA: 19% | Registrado por: admin")


if __name__ == "__main__":
    seed()