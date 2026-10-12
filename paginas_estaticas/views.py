import logging
import os
import re
from urllib.parse import urljoin

from django.conf import settings
from django.shortcuts import render
from django.templatetags.static import static

logger = logging.getLogger(__name__)


def obtener_imagenes_de_carpeta(ruta_base, nombre_carpeta):
    ruta_imagenes = os.path.join(settings.STATICFILES_DIRS[0], ruta_base, nombre_carpeta)
    try:
        if not os.path.isdir(ruta_imagenes):
            logger.warning("La ruta %s no es un directorio válido.", ruta_imagenes)
            return []

        nombres = [
            nombre for nombre in os.listdir(ruta_imagenes)
            if os.path.splitext(nombre)[1].lower() in {'.jpg', '.jpeg'}
            and os.path.isfile(os.path.join(ruta_imagenes, nombre))
        ]
    except OSError as exc:
        logger.warning("No se pudieron leer las imágenes de %s: %s", ruta_imagenes, exc)
        return []

    def clave_natural(nombre):
        partes = re.split(r'(\d+)', nombre.casefold())
        # El nombre completo desempata números equivalentes y diferencias de mayúsculas.
        return ([int(parte) if parte.isdecimal() else parte for parte in partes], nombre)

    return [
        f'{ruta_base}/{nombre_carpeta}/{nombre}'
        for nombre in sorted(nombres, key=clave_natural)
    ]


def index(request):
    # Imágenes de habitaciones
    imagenes_rock = obtener_imagenes_de_carpeta('img/habitaciones', 'rock')
    imagenes_tango = obtener_imagenes_de_carpeta('img/habitaciones', 'tango')
    imagenes_jazz = obtener_imagenes_de_carpeta('img/habitaciones', 'jazz')
    
    # Imágenes de espacios compartidos
    imagenes_patio = obtener_imagenes_de_carpeta('img/esp_compartidos', 'patio')
    imagenes_cocina = obtener_imagenes_de_carpeta('img/esp_compartidos', 'cocina')
    imagenes_living = obtener_imagenes_de_carpeta('img/esp_compartidos', 'living')
    imagenes_barrio = obtener_imagenes_de_carpeta('img/esp_compartidos', 'barrio')
    
    canonical_url = 'https://www.casahuesped53.com.ar/'
    params = {
        'page_title': 'Inicio',
        'site_name': 'Casa Huesped',
        'seo_title': 'Casa Huésped 53 — Alojamiento en La Plata',
        'descripcion': (
            'Conocé Casa Huésped 53, una casona centenaria en el corazón histórico de La Plata. '
            'Habitaciones, espacios compartidos y consultas por WhatsApp.'
        ),
        'canonical_url': canonical_url,
        'social_image_url': urljoin(
            canonical_url, static('img/banners/banner_casahuesped1.jpg')
        ),
        'whatsapp_url': 'https://wa.me/5492213041484',
        'whatsapp_numero': '221 304-1484',
        'imagenes_rock': imagenes_rock,
        'imagenes_tango': imagenes_tango,
        'imagenes_jazz': imagenes_jazz,
        'imagenes_patio': imagenes_patio,
        'imagenes_cocina': imagenes_cocina,
        'imagenes_living': imagenes_living,
        'imagenes_barrio': imagenes_barrio,
    }
    
    return render(request, 'home/index.html', params)