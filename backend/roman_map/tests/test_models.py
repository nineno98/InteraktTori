from roman_map.models import Territorie, Historie
from django.test import TestCase
from django.core.exceptions import ValidationError
import json

class TestModels(TestCase):
    HISTORIE_TYPE_CHOICHES = [
        ('csata','csata'),
        ('esemeny', 'esemény'),
        ]
    def setUp(self):
        
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
            image = None,
            date = 100
        )
    
    def test_historie_date(self):
        self.assertEqual(self.historie.date, 100)

    def test_historie_historie_type(self):
        self.assertIn(self.historie.historie_type, [c[0] for c in self.HISTORIE_TYPE_CHOICHES])
    
    def test_historie_coordinates_invalid(self):
        self.historie.coordinates = "[21,]"
        with self.assertRaises(json.JSONDecodeError):
            json.loads(self.historie.coordinates)
    
    def test_historie_coordinates_valid(self):
        assert json.loads(self.historie.coordinates)

    def test_historie_description(self):
        self.assertEqual(self.historie.description, "test description")

    def test_historie_string_representation(self):
        self.assertEqual(str(self.historie), f"{self.historie.id} {self.historie.name} {self.historie.historie_type}")

    def test_historie_name(self):
        self.assertEqual(self.historie.name, "test_historie")
    
    def test_territorie_string_representation(self):
        self.assertEqual(str(self.territorie), f"{self.territorie.id} {self.territorie.name} {self.territorie.start_date} {self.territorie.end_date}")

    def test_territorie_start_date(self):
        self.assertEqual(self.territorie.start_date, 100)

    def test_territorie_end_date(self):
        self.assertEqual(self.territorie.end_date, 1000)

    def test_territorie__start_date_end_date_valid(self):
        assert not self.territorie.save()
    
    def test_territorie_start_date_end_date_invalid(self):
        self.territorie.start_date = self.territorie.end_date + 1
        with self.assertRaises(ValidationError):
            self.territorie.save()

    def test_territorie_color(self):
        self.assertEqual(self.territorie.color, "#fa0202")

    def test_territorie_coordinates_valid(self):
        assert json.loads(self.territorie.coordinates)
    
    def test_territorie_coordinates_invalid(self):
        self.territorie.coordinates = "[[21, 33] [33, 44]"
        with self.assertRaises(json.JSONDecodeError):
            json.loads(self.territorie.coordinates)

    

    