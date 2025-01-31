from django import forms
from jsonschema import validate, ValidationError as JsonSchemaValidationError
import json
import os
from .models import Territorie, Historie
from .static.files import schema as ValidationsSchema
import pandas as pd

class TerritoriesJSONForm(forms.Form):

    file = forms.FileField(required=True, label="Válasz egy geojson fájlt!")

    def clean_file(self):

        super().clean()

        file = self.cleaned_data.get('file')
        extension = os.path.splitext(file.name)[1].lower()
        if file:
            if extension != '.geojson':
                raise forms.ValidationError('A feltöltött fájl kiterjesztése nem megfelelő!')
        else:
            raise forms.ValidationError('Nincs fájl feltöltve!')
        
        try:
            file_data = file.read().decode('utf-8')
            file.seek(0)
            json_data = json.loads(file_data)
            validate(instance=json_data, schema=ValidationsSchema)
        except OSError:
            raise forms.ValidationError('Hiba a fájl beolvasása közben!')
        except UnicodeDecodeError:
            raise forms.ValidationError('Hiba a fájl dekódolásánál. Nem érvényes utf-8 formátum!')
        except json.JSONDecodeError:
            raise forms.ValidationError('Hibás a JSON formátum!')
        except JsonSchemaValidationError as e:
            raise forms.ValidationError(f'Json validációs hiba: {e.message}')
        except Exception as e:
            raise forms.ValidationError(str(e))
        
        return file
    
    def save(self):
        uploaded_file = self.cleaned_data.get('file')
        try:
            file_data = uploaded_file.read().decode('utf-8')
            json_data = json.loads(file_data)
            feature_type = json_data.get('type')
            if feature_type == "FeatureCollection":
                if "features" in json_data:
                    features = json_data.get('features')
                    for item in features:
                        Territorie.objects.create(
                            name=item["properties"]["name"],
                            start_date=int(item["properties"]["start_date"]),
                            end_date=int(item["properties"]["end_date"]),
                            color=item["properties"]["color"],
                            coordinates=item["geometry"]["coordinates"]
                        )
                else:
                    raise forms.ValidationError("A 'features' kulcs hiányzik az objektumból.")
            elif feature_type == "Feature":

                Territorie.objects.create(
                    name=json_data["properties"]["name"],
                    start_date=int(json_data["properties"]["start_date"]),
                    end_date=int(json_data["properties"]["end_date"]),
                    color=json_data["properties"]["color"],
                    coordinates=json_data["geometry"]["coordinates"]
                )
            else:
                raise forms.ValidationError("Menteni kívánt fájl formátuma nem megfelelő.")
        except Exception as e:
            raise forms.ValidationError("Hiba lépett fel a fájl feldolgozása és mentése közben: "+str(e))

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 30, label="Felhasználónév", required=True)
    password = forms.CharField(max_length = 30, label="Jelszó", widget= forms.PasswordInput, required=True)       

class HistorieXLSXImportForm(forms.Form):
    file = forms.FileField(label="XLSX fájl feltöltése")

    def clean_file(self):
        super().clean()
        try:

            file = self.cleaned_data.get('file')

            if not file.name.endswith(".xlsx"):
                raise forms.ValidationError("Csak .xlsx kiterjesztésű fájl engedélyezett.")
            try:
                df = pd.read_excel(file, engine='openpyxl')
            except Exception:
                raise forms.ValidationError("Hibás vagy sérült XLSX fájl.")
            required_columns = {"name", "description", "coordinates", "time", "type", "image"}
            if not required_columns.issubset(df.columns):
                raise forms.ValidationError(f"A fájl nem tartalmazza az összes szükséges mezőket: {required_columns}")
            
            for _, row in df.iterrows():
                coordinates = str(row["coordinates"]).strip()
                if not (coordinates.startswith("[") and coordinates.endswith("]")):
                    raise forms.ValidationError(f"Érvénytelen koordináta formátum: {coordinates}")
                historie_type = str(row['type'])
                print(historie_type)
                if historie_type not in {'csata', 'esemeny'}:
                    raise forms.ValidationError("Érvénytelen típusformátum. a típusnak 'csata' vagy 'esemeny' kell lennie.")

            self.cleaned_data["df"] = df
        except Exception as e:
            print(e)
            raise forms.ValidationError(f"clean_file: Hiba: {e}")
            
        return file
    def save(self):
        df = self.cleaned_data.get("df")

        for _, row in df.iterrows():
            Historie.objects.create(
                name=row["name"],
                description=row["description"],
                coordinates = row["coordinates"],
                historie_type = row["type"].lower(),
                image = row["image"] if pd.notna(row["image"]) else None,
                date = row["time"]

            )

        

