# Casa Huésped 53

Aplicación web en producción para un alojamiento real en La Plata, desarrollada con Python y Django. El proyecto documenta tanto la evolución del backend como su testing, despliegue y mantenimiento en un servidor Linux.

**[Ver sitio en producción](https://www.casahuesped53.com.ar/)**

## Problema y alcance

El alojamiento necesitaba una presencia web para presentar sus habitaciones, espacios y servicios, y facilitar consultas por WhatsApp. La solución es una landing renderizada en servidor, con mantenimiento proporcional al tamaño del proyecto.

## Funcionalidades reales

- Presentación de las habitaciones Rock, Tango y Jazz, espacios compartidos, servicios, ubicación y reglamento.
- Galerías Fancybox independientes por espacio; JPG/JPEG con filtrado y orden natural determinista.
- Contacto por WhatsApp con URL centralizada, enlace de email y mapa.
- Metadatos SEO y sociales, canonical, `robots.txt` y sitemap de la única página pública.
- Mejoras puntuales de semántica HTML, textos alternativos y nombres accesibles de controles.

No incluye reservas, cuentas de huéspedes, pagos, formulario Django de consultas ni emails automáticos.

## Stack y arquitectura

| Área | Tecnología |
| --- | --- |
| Backend | Python 3.10.12 en producción; Django 5.2.17 LTS; Django Templates |
| Persistencia | SQLite |
| Frontend existente | HTML, CSS/SCSS, Bootstrap, JavaScript, jQuery, GSAP/ScrollTrigger y Fancybox |
| Despliegue | DigitalOcean, Ubuntu 22.04.5 LTS, Nginx 1.18.0 y Gunicorn 23.0.0; HTTPS |

```text
Cliente → Nginx → Gunicorn → Django → SQLite
           └── archivos estáticos
```

Gunicorn utiliza un worker mediante socket Unix. Nginx sirve los estáticos y consolida las variantes del dominio en la URL canónica HTTPS con www mediante redirecciones 301.

## Trabajo técnico realizado

- Migración de Django 4.2 a 5.2 LTS y actualización de Ubuntu 20.04 a 22.04.
- Saneamiento del repositorio e historial: exclusión de secretos, configuración privada, SQLite y estáticos generados.
- Optimización del conjunto fuente de imágenes: 70 JPG finales y reducción aproximada del 34,8 %, sin atribuirle métricas de carga no medidas.
- Incorporación de tests de landing, galerías, contacto, metadatos, rastreo y semántica.
- Correcciones puntuales de accesibilidad y tres hitos de SEO técnico desplegados.
- Mantenimiento del servidor: recuperación de un incidente de kernel/initramfs, recreación de entornos Python y ajuste de workers, swap, logs y espacio de disco.

El detalle y la evidencia histórica están en [historial técnico](docs/historial-tecnico.md) y [producción](docs/produccion.md).

## Qué demuestra este proyecto

- Mantenimiento y evolución de una aplicación Django real en producción.
- Testing automatizado para prevenir regresiones.
- Despliegue y operación con Nginx/Gunicorn y troubleshooting en Linux.
- Manejo de configuración sensible fuera de Git.
- Decisiones técnicas proporcionales al alcance y los recursos disponibles.

## Testing

**25 tests automatizados** con Django `SimpleTestCase`, sin dependencias adicionales de testing. Cubren respuesta y contexto de la landing, WhatsApp, grupos Fancybox, filtrado/orden y errores de galerías, metadatos, robots/sitemap, headings y alt.

```bash
python manage.py check
python manage.py test
```

Las pruebas de galerías usan directorios temporales y `override_settings`. No ejecutan JavaScript ni sustituyen el QA visual; el README de `static_dev/js/tests/` pertenece a Bootstrap, no a la suite propia.

## Decisiones y límites

Django y sus templates mantienen una base conocida y comprobable. SQLite es suficiente para el alcance actual, sin un flujo de reservas ni carga de escritura que justifique otro motor; requiere backups y una restauración probada. Un worker de Gunicorn responde a los recursos y tráfico actuales, con capacidad a revisar si cambian.

`static_dev/` contiene los assets versionados; `static/` es salida de `collectstatic`. `settings.py`, SQLite, secretos y entornos no se versionan. `collectstatic` no compila SCSS: no hay un build Sass reproducible aprobado y persiste la doble inclusión de Bootstrap.

## Estado al 14/10/2026

Producción ejecuta `d3f67c5`, con HTTPS operativo, 25 tests aprobados y SEO hitos 1–3 desplegados y verificados. El cliente está conforme y el QA básico de desktop/móvil fue aprobado, según la confirmación del responsable. Esta revisión documental no accede al servidor.

La seguridad mínima fue revisada: `DEBUG=False`, hosts restringidos y cookies de sesión/CSRF seguras; HSTS y HTTP→HTTPS se gestionan en Nginx. Sigue pendiente sustituir la ejecución de Gunicorn como root, hacer reproducible su dependencia y probar una restauración completa de backups. Hay deuda visual menor no bloqueante en espaciado/alineación de habitaciones y variaciones de altura de fotografías en móvil. No se presenta esta revisión como una auditoría integral de seguridad o accesibilidad.

## Instalación local

Usar Python compatible con Django 5.2; producción utiliza 3.10.12. Desde el repositorio:

```bash
git clone https://github.com/P4bloh/CasaHuesped.git
cd CasaHuesped
python -m venv .venv
```

Activar con `.\.venv\Scripts\Activate.ps1` en PowerShell o `source .venv/bin/activate` en Linux/macOS. Luego:

```bash
python -m pip install -r requirements.txt
```

Copiar `casahuesped/settings.example.py` a `casahuesped/settings.py` y revisar sus valores locales:

```powershell
# Windows PowerShell
Copy-Item casahuesped/settings.example.py casahuesped/settings.py
```

```bash
# Linux/macOS
cp casahuesped/settings.example.py casahuesped/settings.py
```

```bash
python manage.py migrate
python manage.py check
python manage.py test
python manage.py runserver
```

El ejemplo usa hosts locales y `DEBUG` activado por defecto. Lee `SECRET_KEY` y `DEBUG` del entorno del proceso, sin cargar `.env` automáticamente; no es configuración de producción. Con `DEBUG=True`, `runserver` sirve los assets desde `static_dev/` sin `collectstatic`. No usar `runserver` en producción. `requirements.txt` fija Django; Gunicorn está instalado en el servidor, pero aún no está declarado allí.

## Documentación técnica

- [Estado y handoff](docs/estado.md): situación actual y pendientes.
- [Producción](docs/produccion.md): arquitectura, seguridad, operación y rollback.
- [Historial técnico](docs/historial-tecnico.md): evolución e incidentes, con corte histórico al 07/10/2026.
- [AGENTS.md](AGENTS.md): instrucciones y límites para agentes.

## Propiedad y licencias

El código propio se presenta como trabajo profesional y de portfolio, sin conceder una licencia abierta de reutilización en esta entrega. La marca, textos, fotografías, logos y demás assets del cliente se utilizan con autorización para el proyecto y portfolio; no se otorgan derechos de reutilización a terceros. Bootstrap, jQuery y las demás librerías conservan sus propias licencias. Ver [propiedad y atribuciones de terceros](THIRD_PARTY_NOTICES.md).

## Uso de IA

Codex se utilizó como agente de apoyo en tareas delimitadas de revisión, implementación, pruebas y documentación. Los cambios tuvieron revisión manual, validaciones y aprobación del responsable antes de commits y despliegues. La responsabilidad sobre el alcance y la aceptación del resultado se mantuvo en la persona a cargo del proyecto.
