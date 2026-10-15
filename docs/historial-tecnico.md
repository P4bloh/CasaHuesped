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

Durante la actualización de Ubuntu 20.04 a 22.04 se produjo un kernel panic relacionado con un initramfs demasiado grande para un servidor de memoria limitada.

Se recuperó el arranque usando temporalmente un kernel anterior. Después se ajustó la selección de módulos del initramfs, reduciendo su tamaño aproximadamente un 54 %, y se validó el kernel actualizado mediante un arranque de prueba antes de establecerlo como habitual. Se conservó una alternativa de arranque para recuperación.

El caso aporta experiencia de diagnóstico y recuperación en Linux. Las versiones de kernel, ubicaciones y pasos específicos del servidor activo no se incluyen en esta versión pública.

## Recreación de entornos y clon limpio de producción

Tras actualizar el sistema operativo se recrearon los entornos Python para usar el intérprete compatible con el sistema actualizado.

La migración de producción utilizó un clon limpio del repositorio saneado, conservando la configuración privada y SQLite fuera de Git. Se guardó una copia del despliegue y entorno anteriores como recurso de rollback, separado del checkout activo.

Antes de la activación se validaron `check`, tests, migraciones, `collectstatic` y Gunicorn aislado. La comprobación final informada fue una respuesta `200` por HTTPS público. Esta revisión documental no vuelve a ejecutar esas operaciones sobre el servidor.

## Ajuste de recursos y limpieza

Gunicorn se redujo de 3 a 1 worker por los recursos disponibles y el tráfico actual. Se mantuvo Nginx como servidor frontal, comunicándose con Gunicorn mediante un socket Unix y sirviendo los archivos estáticos.

Se habilitó swap, se limitó el crecimiento de logs y se limpiaron archivos para recuperar margen de disco. Estos ajustes forman parte del mantenimiento operativo; las rutas internas y parámetros concretos se omiten del repositorio público.

## Continuidad

Gunicorn todavía ejecuta como root y su dependencia no es reproducible desde requirements. La restauración completa de backups todavía no está probada. Queda definir la política definitiva de retención/eliminación de la copia de rollback y del kernel fallback, cuya existencia fue confirmada; las ubicaciones se mantienen fuera de esta documentación pública.

La siguiente etapa prevista es auditar enlaces, SEO, analítica, UX/slider, accesibilidad y rendimiento. Consultar [estado](estado.md) para el handoff vivo y [producción](produccion.md) para las decisiones y límites operativos.
