from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit

from django.templatetags.static import static
from django.test import SimpleTestCase, override_settings


class EnlacesParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.enlaces = []
        self.contenidos = []
        self.enlace_actual = None
        self.metas = []
        self.links = []
        self.titulos = []
        self.en_titulo = False

    def handle_starttag(self, tag, attrs):
        if tag == 'meta':
            self.metas.append(dict(attrs))
        elif tag == 'link':
            self.links.append(dict(attrs))
        elif tag == 'title':
            self.titulos.append('')
            self.en_titulo = True
        if tag == 'a':
            atributos = dict(attrs)
            self.enlaces.append(atributos)
            self.enlace_actual = {'attrs': atributos, 'texto': '', 'botones': 0}
            self.contenidos.append(self.enlace_actual)
        elif tag == 'button' and self.enlace_actual is not None:
            self.enlace_actual['botones'] += 1

    def handle_data(self, data):
        if self.en_titulo:
            self.titulos[-1] += data
        if self.enlace_actual is not None:
            self.enlace_actual['texto'] += data

    def handle_endtag(self, tag):
        if tag == 'title':
            self.en_titulo = False
        if tag == 'a':
            self.enlace_actual = None


class HomePageSmokeTests(SimpleTestCase):
    def setUp(self):
        super().setUp()
        temporal = TemporaryDirectory()
        self.addCleanup(temporal.cleanup)
        static_dir = Path(temporal.name)
        for ruta_base, carpetas in (
            ('img/habitaciones', ('rock', 'tango', 'jazz')),
            ('img/esp_compartidos', ('patio', 'cocina', 'living', 'barrio')),
        ):
            for nombre in carpetas:
                carpeta = static_dir / ruta_base / nombre
                carpeta.mkdir(parents=True)
                for numero in (2, 1):
                    (carpeta / f'{nombre}{numero}.jpg').touch()

        configuracion = override_settings(STATICFILES_DIRS=[str(static_dir)])
        configuracion.enable()
        self.addCleanup(configuracion.disable)

    def obtener_enlaces(self, response):
        return self.obtener_parser(response).enlaces

    def obtener_parser(self, response):
        parser = EnlacesParser()
        parser.feed(response.content.decode(response.charset))
        parser.close()
        return parser

    def test_consultas_son_enlaces_whatsapp_sin_botones_anidados(self):
        response = self.client.get('/')
        consultas = [
            enlace for enlace in self.obtener_parser(response).contenidos
            if enlace['texto'].strip() == 'Consultar'
        ]

        self.assertEqual(len(consultas), 3)
        for enlace in consultas:
            self.assertEqual(enlace['botones'], 0)
            self.assertEqual(enlace['attrs']['href'], response.context['whatsapp_url'])
            self.assertEqual(enlace['attrs'].get('target'), '_blank')
            self.assertIn('btn-consultar', enlace['attrs'].get('class', '').split())

    def test_controles_de_carrusel_tienen_nombre_accesible(self):
        response = self.client.get('/')
        controles = [
            enlace for enlace in self.obtener_enlaces(response)
            if 'data-bs-slide' in enlace
        ]
        carruseles = ('Rock', 'Tango', 'Jazz', 'Patio', 'Cocina', 'Living', 'Barrio')
        esperados = {
            (f'#carousel{nombre}', direccion)
            for nombre in carruseles for direccion in ('prev', 'next')
        }
        self.assertEqual(len(controles), len(esperados))
        self.assertEqual(
            {(enlace.get('href'), enlace['data-bs-slide']) for enlace in controles},
            esperados,
        )
        for enlace in controles:
            with self.subTest(destino=enlace.get('href'), direccion=enlace['data-bs-slide']):
                nombre = 'Imagen anterior' if enlace['data-bs-slide'] == 'prev' else 'Imagen siguiente'
                self.assertEqual(enlace.get('aria-label'), nombre)
                self.assertEqual(enlace.get('role'), 'button')

    def test_home_page_returns_200_and_uses_expected_template(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertIn('page_title', response.context)
        self.assertIn('site_name', response.context)
        self.assertEqual(response.context['page_title'], 'Inicio')
        self.assertEqual(response.context['site_name'], 'Casa Huesped')

    def test_titulo_y_descripciones_seo_son_correctos(self):
        parser = self.obtener_parser(self.client.get('/'))
        titulo = 'Casa Huésped 53 — Alojamiento en La Plata'
        descripcion = (
            'Conocé Casa Huésped 53, una casona centenaria en el corazón histórico de La Plata. '
            'Habitaciones, espacios compartidos y consultas por WhatsApp.'
        )
        self.assertEqual(parser.titulos, [titulo])
        for atributo, nombre, esperado in (
            ('name', 'description', descripcion),
            ('property', 'og:title', titulo),
            ('name', 'twitter:title', titulo),
            ('property', 'og:description', descripcion),
            ('name', 'twitter:description', descripcion),
        ):
            with self.subTest(meta=nombre):
                valores = [m.get('content') for m in parser.metas if m.get(atributo) == nombre]
                self.assertEqual(valores, [esperado])

    def test_canonical_es_unica_y_coincide_con_og_url(self):
        parser = self.obtener_parser(self.client.get('/'))
        canonical = [link.get('href') for link in parser.links
                     if 'canonical' in link.get('rel', '').split()]
        og_urls = [m.get('content') for m in parser.metas if m.get('property') == 'og:url']
        self.assertEqual(canonical, ['https://www.casahuesped53.com.ar/'])
        self.assertEqual(og_urls, canonical)

    def test_imagenes_sociales_usan_el_banner_con_url_https_absoluta(self):
        parser = self.obtener_parser(self.client.get('/'))
        esperado = 'https://www.casahuesped53.com.ar/static/img/banners/banner_casahuesped1.jpg'
        for atributo, nombre in (('property', 'og:image'), ('name', 'twitter:image')):
            with self.subTest(meta=nombre):
                urls = [m.get('content') for m in parser.metas if m.get(atributo) == nombre]
                self.assertEqual(urls, [esperado])
                partes = urlsplit(urls[0])
                self.assertEqual(partes.scheme, 'https')
                self.assertTrue(partes.netloc)

    def test_keywords_no_se_renderiza_ni_se_incluye_en_contexto(self):
        response = self.client.get('/')
        parser = self.obtener_parser(response)
        self.assertFalse(any(m.get('name', '').lower() == 'keywords' for m in parser.metas))
        self.assertNotIn('palabras_claves', response.context)

    def test_todos_los_enlaces_whatsapp_usan_el_numero_internacional(self):
        response = self.client.get('/')
        urls = [
            enlace['href'] for enlace in self.obtener_enlaces(response)
            if enlace.get('href', '').startswith('https://wa.me/')
        ]

        self.assertEqual(urls, ['https://wa.me/5492213041484'] * 5)
        self.assertContains(response, '221 304-1484')

    def comprobar_grupos(self, ruta_base, carpetas):
        response = self.client.get('/')
        grupos = {}
        for enlace in self.obtener_enlaces(response):
            if enlace.get('href', '').startswith(static(f'{ruta_base}/')):
                grupos.setdefault(enlace.get('data-fancybox'), []).append(enlace['href'])

        esperados = {
            f'gallery-{nombre}': [
                static(f'{ruta_base}/{nombre}/{nombre}{numero}.jpg')
                for numero in (1, 2)
            ]
            for nombre in carpetas
        }
        self.assertEqual(grupos, esperados)

    def test_grupos_fancybox_de_habitaciones_son_independientes(self):
        self.comprobar_grupos('img/habitaciones', ('rock', 'tango', 'jazz'))

    def test_grupos_fancybox_de_espacios_compartidos_son_independientes(self):
        self.comprobar_grupos('img/esp_compartidos', ('patio', 'cocina', 'living', 'barrio'))
