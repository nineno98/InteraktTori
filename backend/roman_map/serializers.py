from rest_framework.serializers import ModelSerializer
from .models import Territorie, Historie, CustomPolygon, CustomPoint, CustomUser, CustomDraw
from rest_framework import serializers
import json
import geojson


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name']


class TerritorieSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        
        try:
            geometry = json.loads(instance.coordinates)
            multipolygon = geojson.MultiPolygon(geometry)
            properties = {
                "id": instance.id,
                "name": instance.name,
                "start_date": instance.start_date,
                "end_date": instance.end_date,
                "color": instance.color
            }
            feature = geojson.Feature(properties=properties, geometry=multipolygon)
        
        except json.JSONDecodeError as e:
            raise serializers.ValidationError("Hibás JSON formátum. "+str(e))
        except Exception as e:
            raise serializers.ValidationError("Hiba. "+str(e))
        return feature
    

class HistorieSerializer(serializers.ModelSerializer):
    
    def to_representation(self, instance):
        try:
            geometry = json.loads(instance.coordinates)
            point = geojson.Point(geometry)
            properties = {
                "id": instance.id,
                "name": instance.name,
                "description": instance.description,
                "historie_type":instance.historie_type,
                "image": instance.image
            }
            feature = geojson.Feature(properties=properties, geometry=point)

        except json.JSONDecodeError as e:
            raise serializers.ValidationError("Hibás JSON formátum. "+str(e))
        except Exception as e:
            raise serializers.ValidationError("Hiba. "+str(e))
        return feature
      

class CustomPolygonSerializer(serializers.ModelSerializer):
    
    def to_representation(self, instance):
        
        try:
            geometry = json.loads(instance.coordinates)
            multipolygon = geojson.MultiPolygon(geometry)
            user_data = CustomUserSerializer(instance.created_by).data
            properties = {
                "id": instance.id,
                "name": instance.name,
                "description": instance.description,
                "created_by": user_data
                
            }
            feature = geojson.Feature(properties=properties, geometry=multipolygon)
        
        except json.JSONDecodeError as e:
            raise serializers.ValidationError("Hibás JSON formátum. "+str(e))
        except Exception as e:
            raise serializers.ValidationError("Hiba. "+str(e))
        return feature

class CustomPointSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        try:
            geometry = json.loads(instance.coordinates)
            point = geojson.Point(geometry)
            user_data = CustomUserSerializer(instance.created_by).data
            properties = {
                "id": instance.id,
                "name": instance.name,
                "description": instance.description,
                "created_by": user_data
            }
            feature = geojson.Feature(properties=properties, geometry=point)

        except json.JSONDecodeError as e:
            raise serializers.ValidationError("Hibás JSON formátum. "+str(e))
        except Exception as e:
            raise serializers.ValidationError("Hiba. "+str(e))
        return feature

def geometry_type(type, geometry):
        try:
            match type:
                case "point":
                    return geojson.Point(geometry)
                case "linestring":
                    return geojson.LineString(geometry)
                case "polygon":
                    return geojson.Polygon(geometry)
        except Exception as e:
            raise serializers.ValidationError("Hiba: geometry_type: "+ e)
            
class CustomDrawSerializer(serializers.Serializer):

    created_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    type = serializers.ChoiceField(choices=CustomDraw.TYPE_CHOICHES)

    class Meta:
        model = CustomDraw
        fields = ['id', 'name', 'description', 'coordinates', 'type', 'created_by']

    def create(self, validated_data):
        # Itt is használjuk a validated_data-t, hogy létrehozzuk az objektumot
        return CustomDraw.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Frissítés során csak a coordinates mezőt frissítjük, ha az új adatot tartalmaz
        print("update: "+instance.coordinates)
        coordinates = validated_data.get('coordinates')
        instance.coordinates = coordinates
        print("update_: "+instance.coordinates)
        instance.save()
        return instance
    
    def to_internal_value(self, data):
        request = self.context.get("request", None)
        if request is None:
            raise serializers.ValidationError({"request": "A kérés nem érhető el a serializer contextjében."})
        print("request method: "+request.method)
        if request.method == 'POST':
            if not isinstance(data, dict):
                raise serializers.ValidationError({"geojson": "A megadott adat nem érvényes JSON objektum."})

            #print(data)
            if data.get("type") != "Feature":
                raise serializers.ValidationError({"geojson": "A 'type' mező értékének 'Feature'-nek kell lennie."})

            properties = data.get("properties", {})
            geometry = data.get("geometry", {})

            print("geometry: "+str(geometry))

            if "coordinates" not in geometry or "type" not in geometry:
                raise serializers.ValidationError({"geometry": "A 'geometry' mező hibás vagy hiányzik."})

            try:
                user = CustomUser.objects.get(id=properties["created_by"])
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError({"created_by": "A megadott felhasználó nem létezik."})
            
            return {
                "name": properties.get("name", ""),
                "description": properties.get("description", ""),
                "created_by": user,  # created_by kezelése
                "coordinates": json.dumps(geometry["coordinates"]),  # Koordináták JSON-ként tárolása
                "type": geometry["type"].lower(),  # GeoJSON típus (Point, Polygon stb.)
            }
        elif request.method == 'PATCH':
            if "coordinates" not in data:
                raise serializers.ValidationError({"coordinates": "Ez a mező kötelező frissítéskor."})
            elif not isinstance(data["coordinates"], (list, tuple)):
                raise serializers.ValidationError({"coordinates": "A koordinátáknak listának kell lenniük."})
            return {"coordinates": json.dumps(data["coordinates"])}
        else:
            raise serializers.ValidationError({"method": "Nem támogatott HTTP metódus."})
            

    
    def to_representation(self, instance):
        try:
            geometry = json.loads(instance.coordinates)
            feature_geometry = geometry_type(instance.type, geometry)
            user_data = CustomUserSerializer(instance.created_by).data
            properties = {
                "id": instance.id,
                "name": instance.name,
                "description": instance.description,
                "created_by": user_data
            }
            feature = geojson.Feature(properties=properties, geometry=feature_geometry)
        except json.JSONDecodeError as e:
            raise serializers.ValidationError("Hibás JSON formátum. "+str(e))
        except Exception as e:
            print(e)
            raise serializers.ValidationError(f"Hiba,,,. {repr(e)}")
        return feature

class CustomDrawSerializer_(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    type = serializers.ChoiceField(choices=CustomDraw.TYPE_CHOICHES)

    
    

    class Meta:
        model = CustomDraw
        fields = ['id', 'name', 'description', 'coordinates', 'type', 'created_by']

    def create(self, validated_data):
        # A teljes GeoJSON objektumot dolgozzuk fel
        geometry_data = validated_data.pop('geometry')
        created_by = validated_data.pop('created_by')
        custom_draw = CustomDraw.objects.create(created_by=created_by, **validated_data)
        custom_draw.coordinates = geometry_data['coordinates']  # A koordináták beállítása
        custom_draw.type = geometry_data['type']  # A típus beállítása
        custom_draw.save()
        return custom_draw

    def update(self, instance, validated_data):
        # Frissítéskor a koordinátákat frissítjük
        geometry_data = validated_data.get('geometry')
        if geometry_data:
            instance.coordinates = geometry_data.get('coordinates', instance.coordinates)
            instance.type = geometry_data.get('type', instance.type)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        try:
            geometry = json.loads(instance.coordinates)
            feature_geometry = geometry_type(instance.type, geometry)
            user_data = CustomUserSerializer(instance.created_by).data
            properties = {
                "id": instance.id,
                "name": instance.name,
                "description": instance.description,
                "created_by": user_data
            }
            feature = geojson.Feature(properties=properties, geometry=feature_geometry)
        except json.JSONDecodeError as e:
            raise serializers.ValidationError("Hibás JSON formátum. "+str(e))
        except Exception as e:
            raise serializers.ValidationError("Hiba. "+str(e))
        return feature