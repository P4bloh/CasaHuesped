from django.test import SimpleTestCase

from paginas_estaticas.views import obtener_imagenes_de_carpeta


class ImagenesCarpetaTests(SimpleTestCase):
    def test_obtener_imagenes_de_carpeta_returns_empty_list_when_folder_does_not_exist(self):
        imagenes = obtener_imagenes_de_carpeta(
            'img/no_existe', 'carpeta_inexistente')

        self.assertEqual(imagenes, [])
