# Estado del proyecto y handoff

**Última actualización: 14/10/2026.**

Fuente del estado productivo: confirmación del responsable al 14/10/2026. Esta tarea actualiza documentación sin acceder al servidor. Las métricas de recursos conservan su fecha de medición del 07/10/2026.

## Cierre Portfolio v1.0

El proyecto entra en fase de cierre Portfolio v1.0 como landing de alojamiento real, con foco Backend Python/Django. El cliente está conforme y el sitio funciona correctamente en desktop y móvil; QA visual básico aprobado. Esto no implica una auditoría exhaustiva de accesibilidad, seguridad o rendimiento.

## Estado confirmado en producción

- Rama local revisada: `main`; HEAD y commit desplegado: `d3f67c5` — «Mejora semantica y accesibilidad SEO».
- Python 3.10.12, Django 5.2.17 LTS y SQLite; Ubuntu 22.04.5 LTS, Nginx 1.18.0 y Gunicorn 23.0.0.
- Gunicorn activo con 1 worker mediante socket Unix; todavía ejecuta como root.
- HTTPS público operativo; canonical `https://www.casahuesped53.com.ar/`.
- Variantes HTTP con/sin www y HTTPS sin www consolidadas por Nginx mediante HTTP 301.
- 25 tests automatizados aprobados: 14 de landing/semántica, 9 de galerías y 2 de rastreo SEO.
- SEO hitos 1–3 desplegados y verificados: metadatos/canonical/sociales; robots y sitemap; semántica y alt.
- `/robots.txt` y `/sitemap.xml` responden 200. El sitemap contiene únicamente la URL canónica.
- Landing con habitaciones, espacios, servicios, mapa, reglamento y consultas por WhatsApp. Galerías JPG/JPEG con grupos Fancybox independientes y orden natural.
- No hay reservas, cuentas de huéspedes, pagos, formulario Django de consultas ni emails automáticos.

## Seguridad mínima revisada

`DEBUG=False` y `ALLOWED_HOSTS` limitado a los dominios reales. `SESSION_COOKIE_SECURE=True` y `CSRF_COOKIE_SECURE=True` fueron agregados manualmente al settings privado de producción el 14/10/2026.

Según la verificación confirmada, `manage.py check --deploy` conserva únicamente W004 y W008: Django no configura HSTS ni la redirección HTTP→HTTPS, porque se implementan en Nginx. No son advertencias silenciadas ni ajustes realizados por esta tarea. Ver [producción](produccion.md).

## Rutas operativas confirmadas

| Elemento | Valor |
| --- | --- |
| Código activo | `/root/casahuesped` |
| Entorno virtual | `/root/myenv52` |
| Servicio / directorio de trabajo | `gunicorn.service`; `WorkingDirectory=/root/casahuesped` |
| Socket de Gunicorn y Nginx | `/root/casahuesped.sock` |
| Alias estáticos de Nginx | `/root/casahuesped/static/` y `/root/casahuesped/static_dev/` |

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

## Pendientes conocidos

- Sustituir Gunicorn como root por un usuario de servicio; hacer reproducible su dependencia (23.0.0 en producción, ausente de `requirements.txt`).
- Probar una restauración completa de backups y definir retención/eliminación del rollback y kernel fallback.
- Deuda visual menor no bloqueante: revisar en una tarea futura espaciado/alineación de habitaciones y variaciones de altura del contenedor según las fotos en móvil. No reabrir el experimento responsive como parte del cierre documental.
- Acoplamiento de galerías a `STATICFILES_DIRS[0]`, doble inclusión de Bootstrap y ausencia de un build SCSS reproducible aprobado.
- Analítica y revisiones adicionales de UX, accesibilidad o rendimiento requieren alcance propio; no se afirma una integración de analítica confirmada.

Estos pendientes no se resolvieron en el cierre documental. No hay cambios funcionales o visuales locales pendientes de deploy en esta tarea; solo documentación para revisión.

## Próximo paso y mantenimiento

Revisar y aprobar la documentación de Portfolio v1.0. No hay autorización de commit, push ni deploy. Reservas permanece como posible evolución futura, sin funcionalidad implementada ni compromiso de alcance.

Actualizar fecha, fuente y resultados al confirmar cambios; separar mediciones locales de producción. Mantener coherencia con [producción](produccion.md) y usar [historial técnico](historial-tecnico.md) como registro histórico con corte al 07/10/2026. No incluir secretos.
