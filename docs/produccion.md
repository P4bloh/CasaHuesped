# Producción: arquitectura y operación

**Última actualización documental: 14/10/2026.** Estado productivo actualizado según los hechos confirmados por el responsable al 14/10/2026; los hitos SEO 1–3 están desplegados y verificados. Esta corrección documental no realiza una inspección remota nueva; las métricas de recursos conservan la medición del 07/10/2026. Las rutas registradas son datos operativos, no credenciales; no se incluyen claves, valores privados de settings ni contenido de SQLite.

## Arquitectura actual

El tráfico público HTTPS entra por Nginx. Las peticiones de aplicación llegan a Gunicorn mediante un socket Unix; Gunicorn ejecuta la aplicación WSGI de Django. SQLite aporta persistencia y los archivos estáticos se preparan con `collectstatic` para su publicación por el servidor web.

```text
Cliente HTTPS → Nginx → socket Unix → Gunicorn (1 worker) → Django → SQLite
                 └── archivos estáticos recolectados
```

| Elemento | Versión o valor confirmado |
| --- | --- |
| Sistema operativo | Ubuntu 22.04.5 LTS |
| Kernel | 5.15.0-198-generic |
| Python | 3.10.12 |
| Django | 5.2.17 LTS |
| Gunicorn | 23.0.0; 1 worker; ejecución como root |
| Nginx | 1.18.0 |
| Base de datos | SQLite; versión de la biblioteca no registrada |
| Código activo | `/root/casahuesped` |
| Virtualenv | `/root/myenv52` |
| Transporte Nginx–Gunicorn | Socket Unix `/root/casahuesped.sock`, usado por ambos |
| Servicio systemd | `gunicorn.service` |
| Directorio de trabajo | `WorkingDirectory=/root/casahuesped` |
| Alias estáticos de Nginx | `/root/casahuesped/static/` y `/root/casahuesped/static_dev/` |
| Commit activo | `d3f67c5` — «Mejora semantica y accesibilidad SEO», confirmado al 14/10/2026 |
| Validación pública | Gunicorn activo, HTTPS operativo y robots/sitemap `200`, confirmados al 14/10/2026 |

Comando efectivo de Gunicorn en `gunicorn.service`:

```text
/root/myenv52/bin/gunicorn --workers 1 --bind unix:/root/casahuesped.sock casahuesped.wsgi:application
```

El servicio trabaja en `/root/casahuesped`. Nginx usa el mismo socket y los dos alias estáticos registrados en la tabla.

## Consolidación de dominio — confirmación del responsable al 12/10/2026

Nginx fue configurado manualmente en producción para consolidar estas variantes:

- `http://www.casahuesped53.com.ar/`
- `http://casahuesped53.com.ar/`
- `https://casahuesped53.com.ar/`

hacia `https://www.casahuesped53.com.ar/`, la URL canónica de la landing, mediante HTTP 301. El cambio manual se realizó el 12/10/2026 y las redirecciones se comprobaron directamente con curl. Esta revisión documental no modifica Nginx ni accede a producción.

Los endpoints Django `/robots.txt` y `/sitemap.xml` del hito SEO 2 ya están desplegados y verificados: ambos responden 200 y el sitemap contiene únicamente la canonical HTTPS con www. El hito SEO 3 también está desplegado. La suite actual tiene 25 tests aprobados y el QA básico de desktop/móvil fue aprobado por el responsable. Las métricas de recursos conservan la medición del 07/10/2026.

## Seguridad mínima — confirmación al 14/10/2026

- `DEBUG=False` y `ALLOWED_HOSTS` limitado a los dominios reales.
- `SESSION_COOKIE_SECURE=True` y `CSRF_COOKIE_SECURE=True`, agregados manualmente a la configuración privada de producción el 14/10/2026. No se copia contenido de `settings.py` ni secretos en este documento.
- `manage.py check --deploy` mantiene únicamente `security.W004` (HSTS no configurado en Django) y `security.W008` (redirección HTTP→HTTPS no configurada en Django). Estas medidas se implementan externamente en Nginx, según la verificación confirmada; Django no inspecciona esa configuración. Las advertencias permanecen, no se afirma que fueron silenciadas.
- Gunicorn sigue ejecutándose como root: deuda técnica conocida, no resuelta por esta revisión.

Esta tarea no ejecutó verificaciones remotas ni modificó configuración. No se dispone aquí del valor exacto de HSTS ni se deducen `max-age`, subdominios o preload. La revisión mínima no equivale a una auditoría integral de seguridad.

## Recursos y medidas operativas

- RAM medida: 454 MiB totales y 254 MiB disponibles en la medición final.
- Swap de 1 GiB en `/swapfile`.
- Disco final: 9,6 GB totales, 6,8 GB usados, 2,8 GB libres, 72 %.
- Journal con uso final de 184 MB y límite permanente `SystemMaxUse=200M` en `/etc/systemd/journald.conf.d/10-size.conf`.
- `MODULES=dep` en initramfs.
- Kernel activo `5.15.0-198-generic`; fallback instalado `5.4.0-216`.

Swap ofrece margen frente a presión de memoria; no sustituye la RAM ni garantiza capacidad adicional de procesamiento. La limitación del journal y la limpieza recuperaron espacio. Las cifras son mediciones finales del 07/10/2026.

## Decisiones actuales y razones

| Decisión | Razón y límite |
| --- | --- |
| Mantener Django | El proyecto ya usa sus templates, configuración y tests. Django 5.2 LTS permite continuar sobre una base conocida sin una reescritura para una landing pequeña. |
| Mantener SQLite | El alcance actual no incluye reservas ni una carga de escritura que justifique otro motor. Debe preservarse y respaldarse la base; revisar esta decisión si cambia el alcance o aparecen límites medidos. |
| Gunicorn con 1 worker | Se redujo desde 3 por recursos disponibles y tráfico actual. Es un compromiso de memoria y concurrencia; revisar con mediciones si aumenta el tráfico. |
| Socket Unix | Es el transporte confirmado entre Nginx y Gunicorn en el mismo servidor. Mantener documentados su ruta, propietario y permisos antes de intervenir. |
| `MODULES=dep` | Reduce los módulos incluidos en initramfs a los identificados como necesarios para el sistema, evitando el tamaño excesivo encontrado durante el upgrade. Si cambia hardware o almacenamiento, revisar los módulos requeridos y el procedimiento de recuperación. |
| Entorno Python recreado | Tras actualizar Ubuntu se recrearon entornos para utilizar el Python del sistema actualizado y evitar depender del virtualenv anterior. |
| Clon limpio de producción | Permite desplegar el historial saneado y conservar por separado los datos y la configuración del entorno. |

Gunicorn como root es una condición existente, **no una decisión recomendada para mantener**. Su sustitución por un usuario de servicio queda pendiente.

## Configuración, base y estáticos fuera de Git

- `settings.py`: configuración por entorno que puede contener secretos. Se conserva fuera del control de versiones; el ejemplo versionado es para desarrollo.
- `db.sqlite3`: datos runtime. Git no es un mecanismo de backup ni restore de la base.
- `static/`: salida generada por `collectstatic`, reconstruible a partir de assets y dependencias. No se versiona.
- Secretos y entornos virtuales: privados o específicos de la máquina; tampoco se versionan.

«Fuera de Git» no significa necesariamente «fuera del directorio del proyecto». Conservar los settings y la base del entorno; no sustituirlos por el ejemplo o por una base local al desplegar.

`static_dev/` es la entrada versionada de assets. La vista actual descubre las galerías en `STATICFILES_DIRS[0]`; por ello el despliegue conserva esa entrada además de la salida recolectada. Los alias confirmados de Nginx apuntan a `/root/casahuesped/static/` y `/root/casahuesped/static_dev/`. No se deducen aquí prefijos de URL adicionales a partir de las rutas físicas. `collectstatic` no compila SCSS.

El conjunto fuente optimizado contiene 70 JPG finales, con una reducción aproximada del 34,8 %. Esta métrica describe el conjunto fuente, no una medición del tiempo de carga de la página.

## Despliegue y validaciones

La migración ya realizada usó un clon limpio, conservando settings y SQLite fuera de Git. Se validaron `check`, los tests, migraciones, `collectstatic` y un arranque aislado de Gunicorn antes de activar el código. En aquella migración había 13 tests. El 12/10/2026 se desplegó el hito SEO 1 (`2eca10e`): 19 tests OK en producción antes del deploy y `manage.py check` OK; después se verificaron Gunicorn activo, HTTPS 200 y title, description, canonical, og:url e imágenes sociales en el HTML servido. Al 14/10/2026, producción ejecuta `d3f67c5` con los tres hitos SEO desplegados y verificados, robots/sitemap 200 y 25 tests aprobados. El cliente está conforme; el QA básico de desktop/móvil está aprobado. La deuda visual menor de habitaciones se registra en estado como futura y no bloqueante.

Para un próximo despliegue autorizado, revisar esta secuencia y completar los datos operativos pendientes:

1. Identificar la revisión candidata, el código activo, los datos que se conservarán y el rollback. Confirmar respaldo recuperable y espacio libre antes de cambiar el servicio.
2. Preparar el código y un entorno compatible. `requirements.txt` fija Django 5.2.17; la instalación reproducible de Gunicorn sigue pendiente.
3. Conservar la configuración privada y la base correcta. No crear ni copiar una base de desarrollo sobre producción.
4. Ejecutar `check` y tests con el entorno candidato. Revisar migraciones pendientes, plan e impacto sobre SQLite antes de aplicarlas.
5. Aplicar únicamente las migraciones revisadas y recolectar estáticos en el destino verificado. Estas operaciones escriben archivos/datos y necesitan autorización de despliegue.
6. Probar Gunicorn de forma aislada del socket y servicio activos. Usar un destino temporal autorizado, confirmar respuesta y detener esa instancia al terminar.
7. Activar mediante el procedimiento del servicio confirmado. Verificar HTTPS, estáticos, galerías, enlaces y logs; registrar revisión, resultados y métricas de recursos.

Comandos Django de referencia, desde el directorio candidato y con su configuración revisada:

```bash
python manage.py check
python manage.py test
python manage.py showmigrations
python manage.py migrate --plan
python manage.py migrate
python manage.py collectstatic --noinput
```

En el entorno activo confirmado, el intérprete es `/root/myenv52/bin/python` y el servicio es `gunicorn.service`; no asumir ese entorno para cualquier candidato. El comando efectivo documentado usa el socket activo: una prueba aislada debe usar otro destino para no interferir con producción. Los agentes no deben ejecutar operaciones de producción por iniciativa propia.

## Rollback y recuperación

El rollback de aplicación existente es `/root/casahuesped-old-20261007`, una copia de archivos del despliegue anterior. Su `.git` fue eliminado deliberadamente después de verificar el nuevo despliegue; no es un checkout Git para actualizar o revertir mediante comandos de Git. El entorno Django 4.2 de rollback se conserva en `/root/myenv310`.

El kernel fallback instalado es `5.4.0-216`; el activo es `5.15.0-198-generic`. La recuperación con un kernel anterior corresponde al sistema operativo y es distinta del rollback de aplicación.

La restauración completa de backups todavía no fue probada. La existencia de una copia de archivos y del entorno anterior no demuestra una recuperación completa de datos. Sigue pendiente la política definitiva de retención/eliminación del rollback y del kernel fallback.

Antes del próximo deploy, completar un procedimiento revisable que identifique:

- Código y entorno anterior conservados, y su compatibilidad con la configuración.
- Base y respaldos disponibles; tratamiento de migraciones y escrituras posteriores. Volver a un commit no restaura SQLite.
- Servicio/socket a activar, estáticos compatibles y comprobaciones de HTTPS y logs.
- Criterios para volver atrás y responsable de ejecutar la recuperación.
- Uso del kernel fallback instalado `5.4.0-216` dentro del procedimiento de recuperación del servidor.

No borrar el material de rollback ni kernels de recuperación como parte de una limpieza rutinaria.

## Pendientes

Cambiar el usuario de ejecución de Gunicorn, hacer reproducible su dependencia desde requirements, probar una restauración completa de backups y definir la política definitiva de retención/eliminación del rollback y del kernel fallback. Los detalles de continuidad se mantienen en [estado](estado.md).
