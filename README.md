# Casa Huésped 53

## Descripción

Sitio web de presentación de un alojamiento en La Plata, desarrollado con Django. Muestra habitaciones, espacios compartidos, servicios y vías de contacto, con un diseño responsive.

## Estado actual

La aplicación se encuentra actualmente desplegada. No incluye sistema de reservas, no cuenta con un formulario Django de consultas y no envía emails automáticos. Las consultas se realizan mediante enlaces a WhatsApp.

## Funcionalidades

- Presentación del alojamiento y de sus espacios.
- Sección de habitaciones.
- Galería de imágenes generadas desde la vista.
- Servicios y datos de contacto.
- Enlaces de consulta por WhatsApp.
- Diseño responsive.

## Stack verificado

- Backend: Django 4.2
- Base de datos: SQLite
- Django Templates
- HTML
- CSS / SCSS
- Bootstrap
- JavaScript
- jQuery
- GSAP / ScrollTrigger
- Fancybox
- Git / GitHub
- Producción sobre Ubuntu / DigitalOcean
- Nginx como proxy/servidor frontal
- Gunicorn como servidor WSGI

## Estructura

- `casahuesped/`
- `paginas_estaticas/`
- `templates/`
- `static/`
- `static_dev/`

> `media/` es un directorio runtime opcional y no forma parte de la estructura versionada actual.

## Instalación

```bash
git clone https://github.com/P4bloh/CasaHuesped.git
cd CasaHuesped
```

Crear entorno virtual:

```bash
python -m venv .venv
```

Activación:

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Instalar dependencias:

```bash
python -m pip install -r requirements.txt
```

## Configuración

`settings.py` no se versiona en el repositorio.

Windows:

```powershell
copy casahuesped\settings.example.py casahuesped\settings.py
```

Linux/macOS:

```bash
cp casahuesped/settings.example.py casahuesped/settings.py
```

Luego:

```bash
python manage.py migrate
python manage.py runserver
```

## Tests

```bash
python manage.py test
```

La suite actual cubre la carga principal de la landing page y la función de obtención de imágenes, verificando que:

- `GET /` responde `200`;
- se renderiza `home/index.html`;
- el contexto incluye `page_title` y `site_name`;
- `obtener_imagenes_de_carpeta` devuelve `[]` cuando la carpeta no existe.

## Despliegue

El proyecto se encuentra desplegado en una infraestructura basada en:

- Ubuntu
- DigitalOcean
- Nginx
- Gunicorn
- Django
- SQLite

No se documentan rutas, secretos ni detalles sensibles del entorno de producción.

## Mejoras futuras

- reservas;
- formulario de consultas;
- notificaciones por email;
- mejoras de mantenibilidad.

Estas mejoras figuran como futuras y no implementadas.
