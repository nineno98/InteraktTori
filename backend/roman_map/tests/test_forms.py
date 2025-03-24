from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from roman_map.forms import CustomUserXLSXImportForm
import pandas as pd
from io import BytesIO

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
        
    