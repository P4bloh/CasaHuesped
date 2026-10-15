# Estado del proyecto y handoff

**Última actualización: 14/10/2026.**

Fuente del estado productivo: confirmación del responsable al 14/10/2026. Esta tarea prepara documentación pública sin acceder al servidor; el detalle operativo del entorno activo se omite deliberadamente.

## Cierre Portfolio v1.0

El proyecto entra en fase de cierre Portfolio v1.0 como landing de alojamiento real, con foco Backend Python/Django. El cliente está conforme y el sitio funciona correctamente en desktop y móvil; QA visual básico aprobado. Esto no implica una auditoría exhaustiva de accesibilidad, seguridad o rendimiento.

## Estado confirmado en producción

- Rama de trabajo: `main`; commit desplegado confirmado: `d3f67c5` — «Mejora semantica y accesibilidad SEO». Las revisiones documentales locales posteriores no implican deploy.
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

## Infraestructura y continuidad

Aplicación alojada en DigitalOcean sobre Ubuntu/Linux. Nginx publica HTTPS y estáticos, y se comunica con un worker de Gunicorn mediante un socket Unix. Django renderiza la landing y utiliza SQLite.

Se ajustaron workers, swap y retención de logs para un servidor de recursos limitados. La optimización de imágenes produjo 70 JPG finales y una reducción aproximada del conjunto fuente del 34,8 %.

Se conserva una versión anterior de aplicación y entorno como estrategia de rollback, además de una alternativa de arranque del sistema. Una copia de código no demuestra que se haya probado una restauración completa de datos. Ubicaciones y procedimientos operativos específicos no se incluyen en esta documentación pública.

## Pendientes conocidos

- Sustituir Gunicorn como root por un usuario de servicio; hacer reproducible su dependencia (23.0.0 en producción, ausente de `requirements.txt`).
- Probar una restauración completa de backups y definir retención/eliminación del rollback y kernel fallback.
- Deuda visual menor no bloqueante: revisar en una tarea futura espaciado/alineación de habitaciones y variaciones de altura del contenedor según las fotos en móvil. No reabrir el experimento responsive como parte del cierre documental.
- Acoplamiento de galerías a `STATICFILES_DIRS[0]`, doble inclusión de Bootstrap y ausencia de un build SCSS reproducible aprobado.
- Analítica y revisiones adicionales de UX, accesibilidad o rendimiento requieren alcance propio; no se afirma una integración de analítica confirmada.

Estos pendientes no se resolvieron en el cierre documental. No hay cambios funcionales o visuales locales pendientes de deploy en esta tarea; solo documentación para revisión.

## Próximo paso y mantenimiento

Revisar y aprobar la documentación pública de Portfolio v1.0. El dueño autorizó el uso público del proyecto como trabajo profesional y de portfolio; los assets del cliente no se ofrecen para reutilización. Ver [atribuciones](../THIRD_PARTY_NOTICES.md). No hay autorización de commit, push ni deploy. Reservas permanece como posible evolución futura, sin funcionalidad implementada ni compromiso de alcance.

Actualizar fecha, fuente y resultados al confirmar cambios; separar mediciones locales de producción. Mantener coherencia con [producción](produccion.md) y usar [historial técnico](historial-tecnico.md) como registro histórico con corte al 07/10/2026. No incluir secretos.

## Alcance de la preparación pública

Se generalizaron los documentos operativos y se añadieron atribuciones de terceros, sin cambios de código ni infraestructura. La licencia abierta del código propio no se decidió; los derechos de terceros y del cliente están separados. Esta edición no reescribe el historial: las versiones anteriores conservan el detalle operativo previamente auditado.
