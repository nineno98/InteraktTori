from django.test import Client, TestCase
from roman_map.models import Territorie, Historie, CustomDraw, Quiz, Question, Answer, UserScore, UserAnswer, AncientPlaces
import os
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
import json
import geojson
from http import HTTPStatus
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory


class TestViews(TestCase):
    TYPE_CHOICHES = [
        ("point","Point"),
        ("linestring", "LineString"),
        ("polygon", "Polygon"), 
    ]
    HISTORIE_TYPE_CHOICHES = [
        ('csata','csata'),
        ('esemeny', 'esemény'),
        ]
    QUESTION_TYPES = [
        ('mc', 'Több válasz'),
        ('tf', 'Igaz/Hamis')
    ]
    def setUp(self):
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.TEST_IMAGE_PATH = os.path.join(BASE_DIR, "test_images", "test_image.png")
        assert os.path.exists(self.TEST_IMAGE_PATH), f"Hiba: A fájl nem létezik: {self.TEST_IMAGE_PATH}"

        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            tanulo = False,
            tanar = True,
            first_name = 'test_first_name',
            last_name = "test_last_name"
        )
        

        self.territorie = Territorie.objects.create(
            name = "test_territorie",
            start_date = 100,
            end_date = 1000,
            color = "#fa0202",
            coordinates = '[[[ 21.7433365440549, 15.921404199368197],[21.56656476090123, 15.921404199368197],[21.56656476090123, 12.28978570046047],[21.7433365440549,12.28978570046047],[21.7433365440549,15.921404199368197]]]'
        )

        self.historie = Historie.objects.create(
            name = "test_historie",
            description = "test description",
            coordinates = "[27.31644987181261, 11.17533692739704]",
            historie_type = "esemeny",
            image = self.TEST_IMAGE_PATH,
            date = 100
        )

        
        self.customdraw = CustomDraw.objects.create(
            name = "test_draw",
            description = "test_description",
            coordinates = "[27, 11]",
            type = "point",
            created_by = self.user
        )

        self.current_time = timezone.now()

        

        self.quiz = Quiz.objects.create(
            title = "test_quiz",
            description = "test_description",
            created_by = self.user
        )
        
        self.question = Question.objects.create(
            quiz = self.quiz,
            text = "test_text",
            question_type = "mc",
            points = 1
        )

        self.answer = Answer.objects.create(
            question = self.question,
            text = "test text",
            is_correct = True
        )
        self.userscore = UserScore.objects.create(
            quiz = self.quiz,
            user = self.user,
            total_score = 1
        )
        self.useranswer = UserAnswer.objects.create(
            user = self.user,
            question = self.question,
            selected_answer = self.answer,
            is_correct = True,
            points_awarded = 1
        )
        self.ancientplace = AncientPlaces.objects.create(
            modern_name = "test modern name",
            ancient_name = "test ancient name",
            coordinates = "[10, 10]"
        )

        self.client = Client()
        self.apiclient = APIClient()
        self.factory = APIRequestFactory()

        self.apiclient.login(username = "testuser", password = "testpass" )

        self.fooldal_url = reverse('fooldal')
        self.bejelentkezes_url = reverse('bejelentkezes')
        self.terkep_url = reverse('terkep')
        self.kijelentkezes_url = reverse('kijelentkezes')
        self.jelszovaltas_url = reverse('jelszovaltas')
        self.sajatadatok_url = reverse('sajatadatok')

        self.getTerritories_url = reverse('getTerritories')
        self.getHistories_url = reverse('getHistories')
        self.getAncientPlaces_url = reverse('getAncientPlaces')
        self.customDraws_url = reverse('customDraws')
        self.getTestQuestions_url = reverse('getTestQuestions', kwargs={'quiz_id': 1})

        self.uj_teszt_keszitese_url = reverse('uj_teszt_keszitese')
        self.teszt_reszletei_url = reverse('teszt_reszletei', args=['1'])
        self.kerdes_hozzadasa_url = reverse('kerdes_hozzadasa', args=['1', 'mc'])
        self.teszt_torlese_url = reverse('teszt_torlese', args=['1'])
        self.kerdes_torlese = reverse('kerdes_torlese', args=['1', '1'])
        self.teszt_inditasa_url = reverse('teszt_inditasa', args=['1'])
        self.serve_tile_url = reverse('serve_tile', args=['1','1','1'])
        self.teszteredmenyek_url = reverse('teszteredmenyek', args=['1'])
        self.kerdes_kivalasztasa_url = reverse('kerdes_kivalasztasa', args=['1'])

    def test_fooldal_get(self):
        response = self.client.get(self.fooldal_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'pages/home.html')

    def test_bejelentkezes_get(self):
        response = self.client.get(self.bejelentkezes_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'pages/login.html')
    
    def test_terkep_get(self):
        response = self.client.get(self.terkep_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'pages/map.html')

    def test_kijelentkezes_get(self):
        response = self.client.get(self.kijelentkezes_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.fooldal_url)

    def test_jelszovaltas_get(self):
        response = self.client.get(self.jelszovaltas_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.sajatadatok_url)

    def test_sajatadatok_get(self):
        response = self.client.get(self.sajatadatok_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/user_informations.html')

    def test_getTerritories_get(self):
        response = self.apiclient.get(self.getTerritories_url)
        if response.status_code == 200:
            json_response = geojson.loads(response.content)
            self.assertIsInstance(json_response, geojson.FeatureCollection)
            self.assertIsInstance(json_response["features"][0], geojson.Feature)
        self.assertEqual(response.status_code, HTTPStatus.OK)
            
    def test_getHistories_get(self):
        response = self.apiclient.get(self.getHistories_url)
        if response.status_code == 200:
            json_response = geojson.loads(response.content)
            self.assertIsInstance(json_response, geojson.FeatureCollection)
            self.assertIsInstance(json_response["features"][0], geojson.Feature)
        self.assertEqual(response.status_code, HTTPStatus.OK)
    
    def test_getAncientPlaces_get(self):
        response = self.apiclient.get(self.getAncientPlaces_url)
        if response.status_code == 200:
            json_response = geojson.loads(response.content)
            self.assertIsInstance(json_response, geojson.FeatureCollection)
            self.assertIsInstance(json_response["features"][0], geojson.Feature)
        self.assertEqual(response.status_code, HTTPStatus.OK)
    
    def test_customDraws_get(self):
        response = self.apiclient.get(self.customDraws_url)
        if response.status_code == 200:
            json_response = geojson.loads(response.content)
            self.assertIsInstance(json_response, geojson.FeatureCollection)
            self.assertIsInstance(json_response["features"][0], geojson.Feature)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_customDraws_patch(self):
        patch_data = {
            "id" : self.customdraw.id,
            "coordinates" : [0,0]
        }
        response = self.apiclient.patch(self.customDraws_url, data=patch_data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.customdraw.refresh_from_db()
        self.assertEqual(self.customdraw.coordinates, '[0, 0]')

    def test_customDraws_post(self):
        test_data = {"value":1}
        data = {"type": "Feature","geometry": {"type": "Point","coordinates": [10,40]},"properties": {"name": "ff","description": " ","created_by": "2"}}
        data_ = "{'type': 'Feature','geometry': {'type': 'Point','coordinates': [10,40]},'properties': {'name': 'ff','description': '','created_by': '2'}}"
        #print(type(data))
        #print(json.dumps(data))

        response = self.apiclient.post(self.customDraws_url, data=data, format="json")
        print( response)
        
        
        


    def test_getTestQuestions_get(self):
        response = self.apiclient.get(self.getTestQuestions_url)
        if response.status_code == 200:
            json_response = geojson.loads(response.content)
            self.assertIsInstance(json_response, list)
            self.assertEqual(json_response[0]['id'], self.question.id)
            self.assertEqual(json_response[0]['text'], self.question.text)
            self.assertEqual(json_response[0]['points'], self.question.points)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    
            
