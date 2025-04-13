from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from roman_map.forms import CustomUserXLSXImportForm, AncientPlacesJSONForm, TerritoriesJSONForm, LoginForm, HistorieXLSXImportForm
import pandas as pd
from io import BytesIO
import json

class TestCustomUserXLSXImportForm(TestCase):
    def setUp(self):
        
        data = {
            "first_name": ["Teszt", "Tanar"],
            "last_name": ["Teszt", "Tanulo"],
            "status": ["tanar", "tanulo"],
            "password": ["Password193", "Password4116"]
        }
        
        df = pd.DataFrame(data)
        
        
        with BytesIO() as bfile:
            df.to_excel(bfile, index=False, engine='openpyxl')
            bfile.seek(0)
            self.test_file = SimpleUploadedFile("test_file.xlsx", bfile.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    def test_form_valid_file(self):
        form_data = {}
        file_data = {'file': self.test_file}
        form = CustomUserXLSXImportForm(data=form_data, files=file_data)
        
        self.assertTrue(form.is_valid())
        self.assertIn("df", form.cleaned_data)

    def test_form_invalid_file(self):
        form_data = {}
        invalid_file = SimpleUploadedFile("test_file.txt", b"Not an excel file", content_type="text/plain")
        file_data = {'file': invalid_file}
        form = CustomUserXLSXImportForm(data=form_data, files=file_data)

        self.assertFalse(form.is_valid())
        self.assertIn("file", form.errors)
        self.assertEqual(form.errors['file'], ["clean_file: Hiba: ['Csak .xlsx kiterjesztésű fájl engedélyezett.']"])
        
class TestAncientPlacesJSONForm(TestCase):
    def test_valid_geojson(self):
        data = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [0, 0]},
            "properties": {"ancient_name": "Test", "modern_name": "TestModern"}
        }
        content = json.dumps(data).encode('utf-8')
        file = SimpleUploadedFile("test.geojson", content, content_type="application/geo+json")
        form = AncientPlacesJSONForm(files={'file': file})
        self.assertTrue(form.is_valid())

    def test_invalid_extension(self):
        content = b'{}'
        file = SimpleUploadedFile("test.txt", content, content_type="text/plain")
        form = AncientPlacesJSONForm(files={'file': file})
        self.assertFalse(form.is_valid())
        self.assertIn('A feltöltött fájl kiterjesztése nem megfelelő!', form.errors['file'])

    def test_missing_file(self):
        form = AncientPlacesJSONForm(files={})
        self.assertFalse(form.is_valid())
        self.assertIn('Ennek a mezőnek a megadása kötelező.', form.errors['file'])

    def test_invalid_utf8(self):
        invalid_utf8 = b'\xff\xfe\xfd'
        file = SimpleUploadedFile("test.geojson", invalid_utf8, content_type="application/geo+json")
        form = AncientPlacesJSONForm(files={'file': file})
        self.assertFalse(form.is_valid())
        self.assertIn('Hiba a fájl dekódolásánál. Nem érvényes utf-8 formátum!', form.errors['file'])

    def test_invalid_json_format(self):
        invalid_json = b'{invalid json'
        file = SimpleUploadedFile("test.geojson", invalid_json, content_type="application/geo+json")
        form = AncientPlacesJSONForm(files={'file': file})
        self.assertFalse(form.is_valid())
        self.assertIn('Hibás a JSON formátum!', form.errors['file'])

    def test_schema_validation_error(self):
        bad_data = {"type": "UnknownType"}
        content = json.dumps(bad_data).encode('utf-8')
        file = SimpleUploadedFile("test.geojson", content, content_type="application/geo+json")
        form = AncientPlacesJSONForm(files={'file': file})
        self.assertFalse(form.is_valid())
        self.assertIn('Json validációs hiba:', str(form.errors['file']))

class TestTerritoriesJSONForm(TestCase):
    def test_valid_geojson_file(self):
        valid_geojson = json.dumps({
            "type": "Feature",
            "geometry": {"type": "MultiPolygon", "coordinates": [[[[0,0],[1,0],[1,1],[0,1],[0,0]]]]},
            "properties": {
                "id": 23,
                "name": "Test",
                "start_date": 2,
                "end_date": 100,
                "color": "#000000"
            }
        })
        file = SimpleUploadedFile("test.geojson", valid_geojson.encode('utf-8'), content_type="application/json")
        form = TerritoriesJSONForm(files={"file": file})
        self.assertTrue(form.is_valid())

    def test_invalid_extension(self):
        file = SimpleUploadedFile("test.txt", b"{}", content_type="text/plain")
        form = TerritoriesJSONForm(files={"file": file})
        self.assertFalse(form.is_valid())
        self.assertIn("A feltöltött fájl kiterjesztése nem megfelelő!", form.errors['file'])

    def test_no_file_uploaded(self):
        form = TerritoriesJSONForm(files={})
        self.assertFalse(form.is_valid())
        self.assertIn("Ennek a mezőnek a megadása kötelező.", form.errors['file'][0])

class LoginFormTest(TestCase):
    def test_valid_data(self):
        form = LoginForm(data={
            'username': 'testuser',
            'password': 'secretpass123'
        })
        self.assertTrue(form.is_valid())
    
    def test_missing_username(self):
        form = LoginForm(data={
            'username': '',
            'password': 'secretpass123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_missing_password(self):
        form = LoginForm(data={
            'username': 'testuser',
            'password': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_empty_form(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('password', form.errors)

class HistorieXLSXImportFormTest(TestCase):
    def setUp(self):
        data = [{
            "name": "Csata A",
            "description": "Leírás",
            "coordinates": "[0,0]",
            "time": "1234",
            "type": "csata"
        }]
        
        df = pd.DataFrame(data)
        
        
        with BytesIO() as bfile:
            df.to_excel(bfile, index=False, engine='openpyxl')
            bfile.seek(0)
            self.test_file = SimpleUploadedFile("test_file.xlsx", bfile.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    def test_valid_xlsx_file(self):
        form = HistorieXLSXImportForm(files={"file": self.test_file})
        self.assertTrue(form.is_valid())
        self.assertIn("df", form.cleaned_data)

    def test_invalid_xlsx_file(self):
        invalid_file = SimpleUploadedFile("test_file.txt", b"Not an excel file", content_type="text/plain")
        
        form = HistorieXLSXImportForm(files={"file": invalid_file})
        self.assertFalse(form.is_valid())
        self.assertIn("file", form.errors)
        self.assertEqual(form.errors['file'], ["clean_file: Hiba: ['Csak .xlsx kiterjesztésű fájl engedélyezett.']"])