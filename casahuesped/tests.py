from django.test import SimpleTestCase


class HomePageSmokeTests(SimpleTestCase):
    def test_home_page_returns_200_and_uses_expected_template(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertIn('page_title', response.context)
        self.assertIn('site_name', response.context)
        self.assertEqual(response.context['page_title'], 'Inicio')
        self.assertEqual(response.context['site_name'], 'Casa Huesped')
