# Nuée — Skincare Inventory System

> *Del francés "nube" — inspirado en la fotografía aérea de nubes.*

Aplicación web full-stack de gestión de inventario construida con **Python + Flask**, diseñada para negocios de productos de skincare. Desarrollada como proyecto de grado en INDECAP (Envigado, Colombia).

---

## Funcionalidades

- **Autenticación completa** — Login, registro, recuperación de contraseña con verificación por código OTP enviado al correo
- **Gestión de usuarios** — Roles de administrador y usuario estándar con permisos diferenciados
- **Inventario de productos** — CRUD completo con control de stock mínimo, lote e INVIMA
- **Movimientos de inventario** — Registro de entradas, salidas, daños y vencimientos con generación automática de comprobantes
- **Facturación** — Creación y consulta de facturas con formato de moneda colombiana (COP) y exportación a PDF
- **Clientes y proveedores** — Directorio de contactos con tipos de documento
- **Dashboard** — Métricas en tiempo real: total de productos, alertas de stock bajo, movimientos recientes
- **Movimientos rápidos** — Flujo de "Usuario Ocasional" para operaciones de stock sin registro completo
- **Modo oscuro / claro** — Interfaz adaptativa con sistema de diseño mineral/monocromático
- **Multilenguaje** — Interfaz disponible en español, inglés, francés y portugués (Flask-Babel)

---

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Backend | Python 3, Flask, SQLAlchemy |
| Base de datos | SQL Server (pyodbc + ODBC Driver 17) |
| Migraciones | Flask-Migrate / Alembic |
| Frontend | HTML5, CSS3, Jinja2, Bootstrap, JavaScript |
| Autenticación | Flask-Login, verificación OTP por email |
| Formularios | Flask-WTF (con protección CSRF) |
| Email | Flask-Mail (SMTP Gmail) |
| PDF | Generación desde Python |
| i18n | Flask-Babel |
| Configuración | python-dotenv |

---

## Estructura del proyecto

```
nuee-inventory/
├── app/
│   ├── auth/                      # Login, registro, recuperación de contraseña
│   ├── clienteproveedor/          # Directorio de clientes y proveedores
│   ├── facturas/                  # Facturación, generación de PDF y envío por email
│   ├── insumos/                   # Catálogo de productos e inventario
│   ├── lotes/                     # Control de lotes y vencimientos
│   ├── main/                      # Dashboard principal
│   ├── movimientos/               # Entradas y salidas de inventario
│   ├── static/                    # CSS, JS, imágenes
│   ├── templates/                 # Plantillas Jinja2 por módulo
│   ├── translations/              # Archivos .po/.mo (es, en, fr, pt)
│   ├── extensions.py              # Inicialización de extensiones Flask
│   └── __init__.py                # Application factory (create_app)
├── migrations/                    # Historial de migraciones Alembic
├── app.py                         # Punto de entrada
├── config.py                      # Configuraciones por entorno (Dev / Prod)
├── babel.cfg                      # Configuración para extracción i18n
├── requirements.txt
├── crear_usuario.py               # Script para crear el primer usuario admin
├── seed_nuee.py                   # Script para poblar el catálogo inicial
└── seed_contactos_movimientos.py  # Script para datos de prueba
```

---

## Instalación local

### Requisitos previos

- Python 3.10+
- SQL Server con ODBC Driver 17
- Cuenta Gmail con contraseña de aplicación

### Pasos

```bash
# Clonar el repositorio
git clone https://github.com/ancreart/nuee-inventory.git
cd nuee-inventory

# Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# Instalar dependencias
pip install -r requirements.txt
```

Crear un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=una-clave-secreta-segura
MAIL_USERNAME=tu-correo@gmail.com
MAIL_PASSWORD=tu-contraseña-de-aplicacion
```

```bash
# Aplicar migraciones (requiere que NueeDB exista en SQL Server)
flask db upgrade

# (Opcional) Poblar catálogo inicial de productos
python seed_nuee.py

# Crear el primer usuario administrador
python crear_usuario.py

# Ejecutar la aplicación
python app.py
```

Disponible en `http://127.0.0.1:5000`

---

## Variables de entorno

| Variable | Descripción |
|---|---|
| `SECRET_KEY` | Clave para firmar sesiones y tokens CSRF |
| `MAIL_USERNAME` | Correo Gmail para envío de emails |
| `MAIL_PASSWORD` | Contraseña de aplicación de Gmail (no la contraseña principal) |
| `DATABASE_URL` | Cadena de conexión completa (solo requerida en producción) |

---

## Internacionalización

```bash
# Extraer cadenas del código fuente
pybabel extract -F babel.cfg -o app/translations/messages.pot .

# Actualizar archivos .po existentes
pybabel update -i app/translations/messages.pot -d app/translations

# Compilar traducciones
pybabel compile -d app/translations
```

Idiomas disponibles: `es` (español), `en` (inglés), `fr` (francés), `pt` (portugués).

---

## Sistema de diseño

Nuée usa una identidad mineral/monocromática inspirada en fotografía de nubes:

- **Color principal:** `#111111`
- **Fondo:** `#FAFAFA`
- **Fuente UI:** DM Sans
- **Fuente de marca:** Tenor Sans
- **Referencia visual:** The Ordinary (minimalismo editorial)

---

## Desarrolladora

**Ana María Melo Marín**  
Egresada de Análisis y Desarrollo de Software — INDECAP, Envigado, Colombia  
Marca creativa: [An.creart](https://www.linkedin.com/in/ana-mar%C3%ADa-melo-marin-6438a3214/)

- [LinkedIn](https://www.linkedin.com/in/ana-mar%C3%ADa-melo-marin-6438a3214/)
- [GitHub](https://github.com/ancreart)

---

## Licencia

Proyecto desarrollado como trabajo de grado. Todos los derechos reservados © 2026 Ana María Melo Marín.