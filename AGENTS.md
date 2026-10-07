# Instrucciones para agentes

## Antes de trabajar

- Leer `README.md` y consultar `docs/estado.md` antes de iniciar una tarea importante. Para tareas de operación, leer también `docs/produccion.md`.
- Revisar el estado de Git, los archivos afectados, sus referencias y los tests pertinentes antes de modificar. Respetar cambios existentes del usuario.
- Mantener cambios pequeños, verificables y limitados al objetivo autorizado. Una auditoría o un pendiente documentado no autoriza su implementación.
- Distinguir hechos confirmados, inferencias y pendientes. Indicar fuente y fecha cuando se describa producción; no presentar una comprobación local como verificación del servidor.

## Alcance y decisiones

- Mantener compatibilidad con Django 5.2 LTS. La versión fijada actualmente es 5.2.17; no actualizar dependencias por iniciativa propia.
- Conservar Django, Django Templates y SQLite mientras el alcance no justifique otra decisión. No introducir tecnologías, dependencias ni capas innecesarias.
- La aplicación actual es una landing con consultas por WhatsApp. No implementar reservas, formularios ni emails sin una tarea explícita.
- No tocar producción directamente. Un cambio local no autoriza acceso al servidor, despliegues, reinicios ni ajustes de configuración; requieren autorización explícita y un procedimiento revisado.
- No hacer commit, push ni otras operaciones de publicación sin autorización explícita. No descartar cambios ajenos ni reescribir historial por iniciativa propia.

## Datos y archivos

- No versionar `casahuesped/settings.py`, `db.sqlite3`, secretos, `.env`, entornos virtuales ni la salida generada de `collectstatic` en `static/`.
- No copiar secretos ni datos privados en documentación, diffs, ejemplos o salidas de comandos. Usar valores de ejemplo cuando corresponda.
- `static_dev/` contiene los assets versionados que utiliza el proyecto. No eliminar por regla general su CSS preparado ni otros assets necesarios: definir primero qué es entrada y qué es salida reproducible.
- No borrar bases, respaldos, migraciones ni material de rollback como limpieza rutinaria.

## Verificación y entrega

- Ejecutar las verificaciones pertinentes después de cambiar comportamiento. Para cambios de Django: `python manage.py check` y `python manage.py test`, usando el entorno disponible.
- Revisar `git diff`, `git diff --check` y `git status --short` antes de entregar. No instalar paquetes para ejecutar una tarea sin autorización.
- En cambios exclusivamente documentales, comprobar enlaces relativos, consistencia entre documentos y alcance del diff; no es necesario repetir tests de código sin una razón concreta.
- Si una verificación no puede ejecutarse, comunicar la limitación; no declarar éxito sin evidencia.
- Informar archivos modificados, comportamiento resultante, comprobaciones y puntos pendientes. Detenerse para revisión cuando así lo pida el usuario.
- Actualizar `docs/estado.md` cuando una tarea autorizada cambie el estado, los pendientes o la información de handoff. Registrar solo lo confirmado, sin ampliar el alcance a trabajos nuevos.
