# Historial técnico

**Resumen actualizado al 07/10/2026.** Los cambios de infraestructura e incidentes provienen del relato confirmado por el responsable; los hitos de código también tienen referencias en Git. No se asignan fechas exactas a trabajos cuya fecha no fue aportada, ni se presenta este resumen como un registro completo de comandos.

## Saneamiento del repositorio

Se saneó el historial Git para retirar secretos, la base SQLite, archivos estáticos generados y material histórico innecesario. El repositorio conserva código, templates y assets necesarios; `.gitignore` excluye settings privado, SQLite, secretos, virtualenvs y la salida de `collectstatic`.

Esto separa el código reproducible de los datos y la configuración del entorno. La retirada del historial no certifica rotación de credenciales ni una política de respaldos: esos resultados no fueron aportados.

## Assets y pruebas de comportamiento

Se optimizaron imágenes y se eliminó un recurso duplicado. El resultado confirmado es de 70 JPG finales y una reducción aproximada del conjunto fuente del 34,8 %. Git registra el hito `f3aab2f` y la integración de mejoras de portfolio/recursos en `5ca4bd4`. La reducción del conjunto fuente no equivale a una medición de tiempos de carga.

La suite se amplió a 13 tests propios. Se corrigieron los enlaces de WhatsApp con contexto compartido, los grupos de Fancybox y el orden/filtrado de las galerías. Los tests usan directorios temporales para evitar depender del número de fotografías reales; cubren además rutas inválidas y errores de lectura.

Este bloque quedó registrado en `982d3b48f4bc29a709f61a348495a48c0c6b286b`, revisión desplegada al 07/10/2026.

## Django 4.2 → 5.2 LTS

Se migró el proyecto desde Django 4.2 a Django 5.2 LTS, fijando 5.2.17. Git registra la depuración de dependencias en `5484795` y la actualización de Django en `d51d9db`. Producción también utiliza 5.2.17; el desfase previo entre local y producción quedó superado.

Se mantuvieron Django Templates y SQLite para el alcance actual. No se añadieron reservas, formularios de consultas ni emails automáticos.

## Ubuntu 20.04 → 22.04 e incidente de initramfs

Durante la actualización del servidor desde Ubuntu 20.04 a 22.04 se produjo un kernel panic relacionado con un initramfs demasiado grande en una máquina de 512 MB de RAM.

Durante la recuperación se arrancó temporalmente con el kernel `5.4.0-216`. El initramfs de `5.15.0-198-generic` medía aproximadamente 109 MB con `MODULES=most`; después de configurar `MODULES=dep` y regenerarlo quedó en aproximadamente 50 MB, una reducción cercana al 54 %.

Se verificó el kernel `5.15.0-198-generic` primero mediante un arranque de prueba y posteriormente mediante un arranque normal permanente. El estado estable informado es Ubuntu 22.04.5 LTS con ese kernel activo.

El kernel `5.4.0-216` quedó instalado como fallback. La RAM actual medida es de 454 MiB totales y 254 MiB disponibles en la medición final. El dato histórico del servidor de 512 MB y la medición actual son referencias distintas.

## Recreación de entornos y clon limpio de producción

Tras actualizar el sistema operativo se recrearon entornos Python. La aplicación estable utiliza Python 3.10.12 y el virtualenv `/root/myenv52`.

La migración de producción se hizo mediante un clon limpio del repositorio saneado, conservando `settings.py` y `db.sqlite3` fuera de Git. El código activo está en `/root/casahuesped`.

La copia de archivos del despliegue anterior se conserva en `/root/casahuesped-old-20261007`, junto con el entorno de rollback Django 4.2 en `/root/myenv310`. La carpeta de código anterior perdió deliberadamente su `.git` después de verificar el nuevo despliegue.

Antes de la activación se validaron `check`, tests, migraciones, `collectstatic` y Gunicorn aislado. La comprobación final informada fue una respuesta `200` por HTTPS público. Esta revisión documental no vuelve a ejecutar esas operaciones sobre el servidor.

## Ajuste de recursos y limpieza

Gunicorn se redujo de 3 a 1 worker por los recursos disponibles y el tráfico actual. `gunicorn.service` usa `WorkingDirectory=/root/casahuesped` y el comando efectivo:

```text
/root/myenv52/bin/gunicorn --workers 1 --bind unix:/root/casahuesped.sock casahuesped.wsgi:application
```

Nginx usa `/root/casahuesped.sock` y los alias `/root/casahuesped/static/` y `/root/casahuesped/static_dev/`. El entorno cuenta con 1 GiB de swap en `/swapfile`. El límite permanente del journal es `SystemMaxUse=200M`, definido en `/etc/systemd/journald.conf.d/10-size.conf`; su uso final fue de 184 MB.

Se limpiaron archivos y logs para recuperar margen de disco. La medición final del 07/10/2026 es de 9,6 GB totales, 6,8 GB usados, 2,8 GB libres y 72 % de uso.

## Continuidad

Gunicorn todavía ejecuta como root y su dependencia no es reproducible desde requirements. La restauración completa de backups todavía no está probada. Queda definir la política definitiva de retención/eliminación de la copia de rollback y del kernel fallback, cuya existencia y ubicaciones ya están confirmadas.

La siguiente etapa prevista es auditar enlaces, SEO, analítica, UX/slider, accesibilidad y rendimiento. Consultar [estado](estado.md) para el handoff vivo y [producción](produccion.md) para las decisiones y límites operativos.
