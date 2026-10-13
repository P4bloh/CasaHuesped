from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from xml.etree import ElementTree

from django.test import SimpleTestCase, override_settings

from paginas_estaticas.views import obtener_imagenes_de_carpeta


class RastreoSEOTests(SimpleTestCase):
    def test_robots_responde_texto_plano_y_permite_rastreo(self):
        response = self.client.get('/robots.txt')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain; charset=utf-8')
        directivas = [linea.strip() for linea in response.content.decode().splitlines()]
        self.assertEqual(directivas, [
            'User-agent: *',
            'Disallow:',
            'Sitemap: https://www.casahuesped53.com.ar/sitemap.xml',
        ])
        self.assertNotIn('Disallow: /', directivas)

    def test_sitemap_es_xml_valido_con_solo_la_url_canonica(self):
        response = self.client.get('/sitemap.xml')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml; charset=utf-8')
        raiz = ElementTree.fromstring(response.content)
        namespace = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
        self.assertEqual(raiz.tag, f'{namespace}urlset')
        self.assertEqual([nodo.tag for nodo in raiz], [f'{namespace}url'])
        urls = raiz.findall(f'{namespace}url')
        self.assertEqual([nodo.tag for nodo in urls[0]], [f'{namespace}loc'])
        self.assertEqual(
            [nodo.text for nodo in raiz.findall(f'{namespace}url/{namespace}loc')],
            ['https://www.casahuesped53.com.ar/'],
        )
        self.assertNotIn(b'https://casahuesped53.com.ar/', response.content)


class ImagenesCarpetaTests(SimpleTestCase):
    def setUp(self):
        super().setUp()
        temporal = TemporaryDirectory()
        self.addCleanup(temporal.cleanup)
        self.static_dir = Path(temporal.name)
        self.carpeta = self.static_dir / 'img' / 'pruebas' / 'patio'
        self.carpeta.mkdir(parents=True)

        configuracion = override_settings(STATICFILES_DIRS=[str(self.static_dir)])
        configuracion.enable()
        self.addCleanup(configuracion.disable)

    def crear_archivos(self, *nombres):
        for nombre in nombres:
            (self.carpeta / nombre).touch()

    def test_imagenes_se_ordenan_naturalmente(self):
        self.crear_archivos('patio10.jpg', 'patio2.jpg', 'patio9.jpg', 'patio1.jpg')

        self.assertEqual(
            obtener_imagenes_de_carpeta('img/pruebas', 'patio'),
            [
                'img/pruebas/patio/patio1.jpg',
                'img/pruebas/patio/patio2.jpg',
                'img/pruebas/patio/patio9.jpg',
                'img/pruebas/patio/patio10.jpg',
            ],
        )

    def test_orden_es_determinista_ante_numeros_equivalentes(self):
        self.crear_archivos('patio1.jpg', 'patio01.jpg')
        with patch('paginas_estaticas.views.os.listdir', side_effect=[
            ['patio1.jpg', 'patio01.jpg'],
            ['patio01.jpg', 'patio1.jpg'],
        ]):
            primera = obtener_imagenes_de_carpeta('img/pruebas', 'patio')
            segunda = obtener_imagenes_de_carpeta('img/pruebas', 'patio')

        self.assertEqual(primera, segunda)
        self.assertEqual(primera, [
            'img/pruebas/patio/patio01.jpg',
            'img/pruebas/patio/patio1.jpg',
        ])

    def test_acepta_jpg_y_jpeg_sin_distinguir_mayusculas(self):
        nombres = ['foto1.jpg', 'foto2.jpeg', 'foto3.JPG', 'foto4.JPEG',
                   'foto5.JpG', 'foto6.JpEg']
        self.crear_archivos(*nombres)

        self.assertEqual(
            obtener_imagenes_de_carpeta('img/pruebas', 'patio'),
            [f'img/pruebas/patio/{nombre}' for nombre in nombres],
        )

    def test_excluye_extensiones_no_admitidas_y_nombres_sin_extension(self):
        self.crear_archivos(
            'foto.jpg', 'foto.png', 'foto.webp', 'foto.gif', 'foto.txt',
            'fotojpg', 'fotojpeg', 'foto.jpg.bak',
        )

        self.assertEqual(
            obtener_imagenes_de_carpeta('img/pruebas', 'patio'),
            ['img/pruebas/patio/foto.jpg'],
        )

    def test_excluye_subdirectorios_con_extension_de_imagen(self):
        self.crear_archivos('foto.jpg')
        (self.carpeta / 'subcarpeta.jpg').mkdir()
        (self.carpeta / 'subcarpeta.JPEG').mkdir()

        self.assertEqual(
            obtener_imagenes_de_carpeta('img/pruebas', 'patio'),
            ['img/pruebas/patio/foto.jpg'],
        )

    def test_obtener_imagenes_de_carpeta_returns_empty_list_when_folder_does_not_exist(self):
        with self.assertLogs('paginas_estaticas.views', level='WARNING'):
            imagenes = obtener_imagenes_de_carpeta(
                'img/pruebas', 'carpeta_inexistente')

        self.assertEqual(imagenes, [])

    def test_devuelve_lista_vacia_si_la_ruta_es_un_archivo(self):
        (self.carpeta.parent / 'archivo.jpg').touch()

        with self.assertLogs('paginas_estaticas.views', level='WARNING'):
            imagenes = obtener_imagenes_de_carpeta('img/pruebas', 'archivo.jpg')

        self.assertEqual(imagenes, [])

    def test_devuelve_lista_vacia_si_el_directorio_esta_vacio(self):
        self.assertEqual(obtener_imagenes_de_carpeta('img/pruebas', 'patio'), [])

    def test_errores_de_lectura_devuelven_lista_vacia_y_se_registran(self):
        for error in (PermissionError('Sin permiso'), FileNotFoundError('Ya no existe')):
            with self.subTest(error=type(error).__name__):
                with patch('paginas_estaticas.views.os.listdir', side_effect=error):
                    with self.assertLogs('paginas_estaticas.views', level='WARNING'):
                        imagenes = obtener_imagenes_de_carpeta('img/pruebas', 'patio')

                self.assertEqual(imagenes, [])
