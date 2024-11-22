import os
from django.conf import settings
from django.shortcuts import render

def obtener_imagenes_de_carpeta(nombre_carpeta):
    ruta_imagenes = os.path.join(settings.STATICFILES_DIRS[0], 'img', 'habitaciones', nombre_carpeta)
    imagenes = []
    if os.path.exists(ruta_imagenes):
        imagenes = [f'img/habitaciones/{nombre_carpeta}/{img}' for img in os.listdir(ruta_imagenes) if img.endswith('.jpg')]
    else:
        print(f"Error: La ruta {ruta_imagenes} no existe.")
    return imagenes

def index(request):
    imagenes_rock = obtener_imagenes_de_carpeta('rock')
    imagenes_tango = obtener_imagenes_de_carpeta('tango')
    imagenes_jazz = obtener_imagenes_de_carpeta('jazz')
    
    params = {
        'imagenes_rock': imagenes_rock,
        'imagenes_tango': imagenes_tango,
        'imagenes_jazz': imagenes_jazz,
    }
    
    return render(request, 'home/index.html', params)