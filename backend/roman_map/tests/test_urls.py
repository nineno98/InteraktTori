from django.test import SimpleTestCase
from django.urls import resolve, reverse

from roman_map import views

class TestUrls(SimpleTestCase):
    def test_getTerritories_url(self):
        url = reverse('getTerritories')
        self.assertEqual(resolve(url).func, views.getTerritories)
    def test_getHistories_url(self):
        url = reverse('getHistories')
        self.assertEqual(resolve(url).func, views.getHistories)
    def test_getAncientPlaces_url(self):
        url = reverse('getAncientPlaces')
        self.assertEqual(resolve(url).func, views.getAncientPlaces)
    def test_customDraws_url(self):
        url = reverse('customDraws')
        resolved_func = resolve(url).func
        self.assertEqual(resolved_func.view_class, views.CustomDrawsAPIView)
    def test_getTestQuestions_url(self):
        id = 1
        url = reverse('getTestQuestions', kwargs={'quiz_id': id})
        self.assertEqual(resolve(url).func, views.getTestQuestions)
    def test_fooldal_url(self):
        url = reverse('fooldal')
        self.assertEqual(resolve(url).func, views.fooldal)
    def test_login_url(self):
        url = reverse('bejelentkezes')
        self.assertEqual(resolve(url).func, views.bejelentkezes)
    def test_terkep_url(self):
        url = reverse('terkep')
        self.assertEqual(resolve(url).func, views.terkep)
    def test_kijelentkezes_url(self):
        url = reverse('kijelentkezes')
        self.assertEqual(resolve(url).func, views.kijelentkezes)
    def test_jelszovaltas_url(self):
        url = reverse('jelszovaltas')
        self.assertEqual(resolve(url).func, views.jelszovaltas)
    def test_sajatadatok_url(self):
        url = reverse('sajatadatok')
        self.assertEqual(resolve(url).func, views.sajatadatok)
    def test_teszt_url(self):
        url = reverse('teszt')
        self.assertEqual(resolve(url).func, views.teszt)
    def test_uj_teszt_keszitese_url(self):
        url = reverse('uj_teszt_keszitese')
        self.assertEqual(resolve(url).func, views.uj_teszt_keszitese)
    
    def test_teszt_reszletei_url(self):
        id = 1
        url = reverse('teszt_reszletei', kwargs={'quiz_id': id})
        self.assertEqual(resolve(url).func, views.teszt_reszletei)
    def test_kerdes_hozzadasa_url(self):
        q_type = "fv"
        quiz_id = 1
        url = reverse('kerdes_hozzadasa', kwargs={'question_type': q_type, 'quiz_id':quiz_id})
        self.assertEqual(resolve(url).func, views.kerdes_hozzadasa)

    def test_teszt_torlese_url(self):
        id = 1
        url = reverse('teszt_torlese', kwargs={'quiz_id': id})
        self.assertEqual(resolve(url).func, views.teszt_torlese)

    def test_kerdes_torlese_url(self):
        quiz_id = 1
        question_id = 1
        url = reverse('kerdes_torlese', kwargs={'quiz_id': quiz_id, 'question_id':question_id})
        self.assertEqual(resolve(url).func, views.kerdes_torlese)
    def test_teszt_inditasa_url(self):
        quiz_id = 1
        url = reverse('teszt_inditasa', kwargs={'quiz_id': quiz_id})
        self.assertEqual(resolve(url).func, views.teszt_inditasa)
    
    def test_serve_tile_url(self):
        x, y, z = 1,1,1
        url = reverse('serve_tile', kwargs={'x':x, 'y':y, 'z':z})
        self.assertEqual(resolve(url).func, views.serve_tile)
    
    def test_teszteredmenyek_url(self):
        quiz_id = 1
        url = reverse('teszteredmenyek', kwargs={'quiz_id': quiz_id})
        self.assertEqual(resolve(url).func, views.teszteredmenyek)
    
    def test_kerdes_kivalasztasa_url(self):
        quiz_id = 1
        url = reverse('kerdes_kivalasztasa', kwargs={'quiz_id': quiz_id})
        self.assertEqual(resolve(url).func, views.kerdes_kivalasztasa)
    
