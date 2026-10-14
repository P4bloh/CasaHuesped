# Estado del proyecto y handoff

**Última actualización: 14/10/2026.**

Este documento es el punto de entrada para continuar el trabajo. Producción fue accedida y verificada directamente el 12/10/2026, según los hechos confirmados por el responsable. Esta corrección documental del 13/10/2026 no incluye un nuevo acceso. Las métricas de recursos conservan la medición del 07/10/2026, no valores monitorizados en tiempo real.

## Estado confirmado

- Sitio estable en producción; HTTPS público responde `200`.
- Landing de presentación, habitaciones, espacios compartidos, servicios, ubicación, reglamento y consultas por WhatsApp.
- URL internacional de WhatsApp centralizada en la vista; grupos de Fancybox separados por espacio.
- Galerías JPG/JPEG con orden natural, filtrado de archivos y manejo de errores de lectura.
- Suite local actual: 21 tests automatizados (10 de landing, 9 del helper de imágenes y 2 de rastreo SEO). En producción se aprobaron 19 tests antes del deploy del hito SEO 1, el 12/10/2026.
- No hay reservas, formulario Django de consultas ni emails automáticos.

## Stack y versión desplegada

| Elemento | Estado confirmado / fecha |
| --- | --- |
| Aplicación | Python 3.10.12 y Django 5.2.17 LTS |
| Presentación | Django Templates, HTML, CSS/SCSS, Bootstrap, JavaScript, jQuery, GSAP/ScrollTrigger y Fancybox |
| Base de datos | SQLite |
| Servidor | Ubuntu 22.04.5 LTS; kernel 5.15.0-198-generic |
| HTTP / WSGI | Nginx 1.18.0 y Gunicorn 23.0.0 |
| Gunicorn | 1 worker, socket Unix; todavía ejecuta como root |
| Código activo | `/root/casahuesped` |
| Entorno virtual | `/root/myenv52` |
| Servicio systemd / directorio de trabajo | `gunicorn.service`; `WorkingDirectory=/root/casahuesped` |
| Socket compartido por Gunicorn y Nginx | `/root/casahuesped.sock` |
| Alias estáticos de Nginx | `/root/casahuesped/static/` y `/root/casahuesped/static_dev/` |
| Commit desplegado | `2eca10e`, verificado directamente el 12/10/2026 |

El commit desplegado y el baseline local del hito SEO 2 son `2eca10e`. El hito SEO 1 está desplegado y verificado; el hito SEO 2 permanece exclusivamente local. Las versiones y rutas operativas no actualizadas conservan la fotografía del 07/10/2026.

## Servidor y recursos

- RAM medida: 454 MiB totales y 254 MiB disponibles en la medición final.
- Swap: `/swapfile`, 1 GiB.
- Disco final: 9,6 GB totales, 6,8 GB usados, 2,8 GB libres, 72 %.
- Initramfs configurado con `MODULES=dep` tras el incidente de tamaño excesivo.
- Journal: `SystemMaxUse=200M` en `/etc/systemd/journald.conf.d/10-size.conf`; uso final de 184 MB.
- Kernel activo: `5.15.0-198-generic`; kernel fallback instalado: `5.4.0-216`.
- Optimización de imágenes: 70 JPG finales y reducción aproximada del conjunto fuente del 34,8 %.

Comando efectivo de Gunicorn, ejecutado desde `/root/casahuesped` por `gunicorn.service`:

```text
/root/myenv52/bin/gunicorn --workers 1 --bind unix:/root/casahuesped.sock casahuesped.wsgi:application
```

La reducción de workers y la limpieza de archivos/logs recuperaron margen operativo. Antes de tomar decisiones nuevas, volver a medir consumo y espacio libre.

## Rollback temporal

El rollback de aplicación está en `/root/casahuesped-old-20261007`: es una copia de archivos del despliegue anterior. Su `.git` se eliminó deliberadamente después de verificar el nuevo despliegue. Se conserva el entorno Django 4.2 en `/root/myenv310`.

El kernel fallback `5.4.0-216` sigue instalado; el activo es `5.15.0-198-generic`. El rollback de aplicación y el kernel fallback son recursos distintos. La restauración completa de backups todavía no está probada y queda definir la política definitiva de retención/eliminación de ambos recursos. Ver [producción](produccion.md).

## Pendientes técnicos conocidos

- Sustituir la ejecución de Gunicorn como root por un usuario de servicio, mediante una tarea planificada.
- Hacer reproducible la dependencia de Gunicorn: producción usa 23.0.0, pero `requirements.txt` solo declara Django 5.2.17.
- Probar y documentar una restauración completa de backups de SQLite, settings y demás información necesaria para recuperar el servicio.
- Definir la política definitiva de retención/eliminación del rollback de aplicación y del kernel fallback.
- La auditoría previa registró acoplamiento de galerías a `STATICFILES_DIRS[0]`, doble carga de Bootstrap CSS y ausencia de un procedimiento reproducible de compilación SCSS. Revisar su vigencia antes de proponer cambios.

Estos puntos se registran para continuidad; no se resolvieron en esta tarea documental.

## Próximo bloque previsto

Auditar enlaces, SEO, analítica, UX/slider, accesibilidad y rendimiento. Primero comprobar el comportamiento real y las herramientas existentes, luego proponer tareas pequeñas y verificables. Que analítica figure en la auditoría no significa que exista una integración confirmada.

Reservas permanece como posible evolución futura. No forma parte de la funcionalidad actual ni del próximo bloque autorizado.

## Cómo mantener este documento

Actualizar fecha, fuente y resultado al confirmar cambios. Separar resultados locales de los del servidor. Si cambia un dato operativo, actualizar también [producción](produccion.md); registrar hitos relevantes en [historial técnico](historial-tecnico.md). No añadir secretos ni presentar propuestas como trabajo realizado.

## SEO hito 1 — desplegado y verificado el 12/10/2026

Título y descripción aprobados centralizados en la vista, canonical `https://www.casahuesped53.com.ar/` compartida con Open Graph, imagen social HTTPS absoluta usando `banner_casahuesped1.jpg` (1920×1099) y eliminación de meta keywords. Sin cambios de contenido visible, estilos o assets. El commit `2eca10e` fue desplegado: 19 tests OK en producción antes del deploy y `manage.py check` OK. Se verificaron directamente Gunicorn activo, HTTPS 200 y title, description, canonical, og:url e imágenes sociales en el HTML servido.

## SEO hito 2 — rastreo/indexabilidad, implementación local

Implementados `/robots.txt` (texto plano, rastreo permitido y sitemap HTTPS absoluto) y `/sitemap.xml` (XML con únicamente `https://www.casahuesped53.com.ar/`). Ambos endpoints comparten la URL canónica de la landing y no requieren nuevas dependencias ni `django.contrib.sitemaps`. Se agregaron dos tests; la suite local pasa de 19 a 21 tests. Validaciones locales: `manage.py check` sin problemas y los 21 tests aprobados. No se modificaron recursos visuales ni se hizo deploy.

El responsable confirmó el 12/10/2026 que Nginx ya consolida HTTP con/sin www y HTTPS sin www hacia `https://www.casahuesped53.com.ar/`. Nginx fue modificado manualmente el 12/10/2026 y las tres variantes se comprobaron directamente con curl: HTTP 301 desde `http://www.casahuesped53.com.ar/`, `http://casahuesped53.com.ar/` y `https://casahuesped53.com.ar/` hacia la canonical. En producción `/robots.txt` y `/sitemap.xml` continúan en 404 hasta el próximo deploy autorizado. Esta revisión solamente corrige documentación.

## SEO hito 3 — implementación local al 14/10/2026

Baseline local: main, commit 4014b85. El responsable confirmó en esta tarea que los hitos SEO 1 y 2 ya están desplegados y verificados; esto actualiza las referencias históricas anteriores al hito 2 pendiente. No se accedió a producción en esta tarea.

Implementados un h1 único con visually-hidden, misión como párrafo con clase h5 y texto intacto, títulos de espacios como h3 con clase visual h4 y alt corregidos. Los banners del hero usan alt vacío por su función decorativa. Solo se ajustaron las dos referencias GSAP de h4 a .h4 para mantener la animación; sin cambios visuales intencionales, CSS, SCSS ni imágenes modificados. Suite local: 25 tests OK, manage.py check sin problemas. Pendiente de revisión visual local y deploy autorizado; no se hizo commit ni push.
