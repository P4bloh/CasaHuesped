# Casa Huésped 53

Sitio web de presentación de un alojamiento en La Plata, desarrollado con Django. Muestra habitaciones, espacios compartidos, servicios y vías de contacto mediante una landing con diseño responsive.

## Estado actual

Al **07/10/2026**, producción se encuentra estable, usa Django **5.2.17** y responde `200` por HTTPS público. Este estado fue confirmado por el responsable; los datos operativos completos están en [producción](docs/produccion.md).

No hay sistema de reservas, formulario Django de consultas ni emails automáticos. Las reservas son una posible evolución futura, sin implementación ni compromiso de alcance actual.

## Funcionalidades reales

- Presentación del alojamiento y de sus espacios.
- Habitaciones Rock, Tango y Jazz; espacios compartidos: patio, cocina, living y barrio.
- Galerías con grupos independientes de Fancybox.
- Archivos JPG/JPEG, sin distinguir mayúsculas, con orden natural y determinista desde la vista.
- Servicios y datos de contacto.
- Consultas por WhatsApp con URL internacional centralizada en el contexto de la vista.
- Reglamento del alojamiento.
- Diseño responsive.

## Stack verificado

- Backend: Python y Django 5.2 LTS; versión fijada: 5.2.17
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
- Producción: Ubuntu 22.04.5 LTS y Python 3.10.12 sobre DigitalOcean
- Nginx 1.18.0 como proxy/servidor frontal
- Gunicorn 23.0.0 como servidor WSGI, con 1 worker mediante socket Unix

`requirements.txt` declara Django como dependencia directa. Gunicorn existe en producción, pero su instalación todavía no está representada de forma reproducible en el repositorio.

## Estructura

- `casahuesped/`: configuración, URLs, entradas WSGI/ASGI y tests de la landing.
- `paginas_estaticas/`: vista, helper de imágenes y tests de galerías.
- `templates/`: landing y secciones incluidas.
- `static_dev/`: assets versionados usados como entrada de archivos estáticos.
- `static/`: salida generada por `collectstatic`; no se versiona.
- `docs/`: estado vivo, producción e historial técnico.
- `AGENTS.md`: instrucciones persistentes para agentes.

> `media/` es un directorio runtime opcional y no forma parte de la estructura versionada actual.

## Instalación

```bash
git clone https://github.com/P4bloh/CasaHuesped.git
cd CasaHuesped
```

Usar una versión de Python compatible con Django 5.2. La versión confirmada en producción es Python 3.10.12. Crear el entorno virtual:

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

`casahuesped/settings.py` contiene la configuración de cada entorno y puede incluir secretos; no se versiona. Copiar el ejemplo para desarrollo local:

Windows:

```powershell
copy casahuesped\settings.example.py casahuesped\settings.py
```

Linux/macOS:

```bash
cp casahuesped/settings.example.py casahuesped/settings.py
```

Revisar la configuración local y luego ejecutar:

```bash
python manage.py migrate
python manage.py check
python manage.py test
python manage.py runserver
```

El ejemplo está orientado a desarrollo, con hosts locales y `DEBUG` activado por defecto. Lee `SECRET_KEY` y `DEBUG` desde variables del proceso; no carga un archivo `.env` automáticamente. No usarlo sin adaptar en producción.

Con `DEBUG=True`, `runserver` sirve los assets desde `static_dev/`; no se necesita generar `static/` para ese flujo local. `runserver` es exclusivamente para desarrollo. La compilación SCSS aún no tiene un procedimiento documentado reproducible; `collectstatic` recolecta archivos, no compila SCSS.

`db.sqlite3` contiene datos runtime y no se versiona: su conservación depende de respaldos, no de Git. Settings privado, secretos, entornos virtuales y `static/` están excluidos mediante `.gitignore`. El historial fue saneado para retirar secretos, SQLite, estáticos generados y archivos históricos innecesarios.

## Tests

```bash
python manage.py test
```

La suite propia consta de **13 tests automatizados** con `SimpleTestCase`, sin dependencias de testing adicionales:

- Respuesta, template y contexto de la landing.
- Los cinco enlaces WhatsApp con el número internacional correcto.
- Grupos Fancybox independientes de habitaciones y espacios compartidos.
- Orden natural y desempate determinista de imágenes.
- Admisión de JPG/JPEG en distintas mayúsculas y exclusión de otras extensiones y subdirectorios.
- Carpetas inexistentes, rutas que son archivos, directorios vacíos y errores de lectura con logging.

Los tests usan directorios temporales y `override_settings` para aislarse de las fotografías reales. No ejecutan JavaScript ni reemplazan una revisión visual en navegador. El README de `static_dev/js/tests/` pertenece a Bootstrap, no a la suite propia.

## Documentación técnica

- [Estado vivo y handoff](docs/estado.md): consultar antes de una tarea importante.
- [Producción](docs/produccion.md): arquitectura, recursos, decisiones, despliegue y rollback.
- [Historial técnico](docs/historial-tecnico.md): evolución y recuperación del servidor.
- [Instrucciones para agentes](AGENTS.md): alcance, verificaciones y protección de datos.

El próximo bloque previsto es auditar enlaces, SEO, analítica, UX/slider, accesibilidad y rendimiento. Los pendientes y los puntos no confirmados se mantienen en `docs/estado.md`. No se incluyen secretos en esta documentación.
