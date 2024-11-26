import os
import logging
from django.conf import settings
from django.shortcuts import render

logger = logging.getLogger(__name__)

def obtener_imagenes_de_carpeta(ruta_base, nombre_carpeta):
    ruta_imagenes = os.path.join(settings.STATICFILES_DIRS[0], ruta_base, nombre_carpeta)
    imagenes = []
    if os.path.exists(ruta_imagenes):
        imagenes = [f'{ruta_base}/{nombre_carpeta}/{img}' for img in os.listdir(ruta_imagenes) if img.endswith(('.jpg', 'jpeg'))]
    else:
        logger.error(f"La ruta {ruta_imagenes} no existe.")
    return imagenes

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
    
    params = {
        'page_title': 'Inicio',
        'site_name': 'Casa Huesped',
        'palabras_claves': 'hospedaje, casa, alquiler, vacaciones',
        'descripcion': 'Bienvenidos a Casa Huesped, tu hogar lejos de casa',
        'imagenes_rock': imagenes_rock,
        'imagenes_tango': imagenes_tango,
        'imagenes_jazz': imagenes_jazz,
        'imagenes_patio': imagenes_patio,
        'imagenes_cocina': imagenes_cocina,
        'imagenes_living': imagenes_living,
        'imagenes_barrio': imagenes_barrio,
    }
    
    return render(request, 'home/index.html', params)