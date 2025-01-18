from django import forms
from jsonschema import validate, ValidationError as JsonSchemaValidationError
import json
import os
from .models import Territorie
from .static.files import schema as ValidationsSchema

class TerritoriesJSONForm(forms.Form):
    file = forms.FileField()

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
        
        return file
    
    def save(self):
        uploaded_file = self.cleaned_data.get('file')
        try:
            json_data = json.loads(uploaded_file)
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
                            geometry=item["geometry"]["coordinates"]
                        )
                else:
                    raise KeyError("A 'features' kulcs hiányzik az objektumból.")
            elif feature_type == "Feature":
                Territorie.objects.create(
                    name=item["properties"]["name"],
                    start_date=int(item["properties"]["start_date"]),
                    end_date=int(item["properties"]["end_date"]),
                    color=item["properties"]["color"],
                    geometry=item["geometry"]["coordinates"]
                )
            
            else:
                raise KeyError("Menteni kívánt fájl formátuma nem megfelelő.")
        except Exception as e:
            raise forms.ValidationError("Hiba lépett fel a fájl feldolgozása és mentése közben: "+str(e))

        

        
        

