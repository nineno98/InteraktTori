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

    class Meta:
        model = CustomDraw
        fields = ['id', 'coordinates', 'name', 'description', 'type']
    #status = serializers.CharField()
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required = False)
    geojson_data = serializers.JSONField(required = False)
    
    
    def validate_geojson_data(self, data):
        try:
            if not isinstance(data, dict):
                raise serializers.ValidationError("A geojson_data nem érvényes JSON objektum.")
            elif data["type"] != "Feature":
                raise serializers.ValidationError("A geojson_data 'type' mezőjének 'Feature'-nek kell lennie.")
            elif "geometry" not in data:
                raise serializers.ValidationError("A geojson_data nem tartalmaz 'geometry' mezőt.")
            

            properties = data["properties"]
            if "name" not in properties:
                raise serializers.ValidationError("A properties mezőben kötelező a 'name' kulcs.")
            if "description" not in properties:
                raise serializers.ValidationError("A properties mezőben kötelező a 'description' kulcs.")
            
            geometry = data["geometry"]
            geometry_types = {"Point", "Polygon", "LineString"}
            if not isinstance(geometry, dict) or "coordinates" not in geometry or "type" not in geometry:
                raise serializers.ValidationError("A geometry formátuma hibás.")
            elif geometry["type"] not in geometry_types:
                raise serializers.ValidationError("A geometry típusa hibás.")
            
            coordinates = geometry["coordinates"]
            if geometry["type"] == "Point":
                if len(coordinates) != 2:
                    raise serializers.ValidationError("A Point típusú geometriának pontosan 2 koordinátát kell tartalmaznia.")
            elif geometry["type"] == "Polygon":
                if len(coordinates) < 1:
                    raise serializers.ValidationError("A Polygon típusú geometriának legalább egy koordinátát kell tartalmaznia.")
            elif geometry["type"] == "LineString":
                if len(coordinates) < 2:
                    raise serializers.ValidationError("A LineString típusú geometriának legalább kettő koordinátát kell tartalmaznia.")

        except Exception as e:
            raise serializers.ValidationError("Hiba: validate_types: "+str(e))
        return data
        
            
    def create(self, validated_data):
        geojson_data = validated_data.get('geojson_data')
        user = validated_data.get('user')
        
        custom_draw = CustomDraw.objects.create(
            name = geojson_data["properties"]["name"],
            description = geojson_data["properties"]["description"],
            coordinates = geojson_data["geometry"]["coordinates"],
            type = geojson_data["geometry"]["type"].lower(),
            created_by = user
        )
        return custom_draw

    def update(self, instance, validated_data):
        # Csak a 'coordinates' mezőt frissítjük
        print(validated_data)
        print(str(instance))
        coordinates = validated_data.get('coordinates', None)
        print('steri: '+str(coordinates))
        if coordinates:
            print(f"Frissített koordináták: {coordinates}")
            instance.coordinates = coordinates  # Frissítjük a koordinátákat

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

class GeometrySerializer(serializers.Serializer):
    type = serializers.CharField()
    coordinates = serializers.ListField(child=serializers.FloatField())

class CustomDrawSerializer_(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    type = serializers.ChoiceField(choices=CustomDraw.TYPE_CHOICHES)

    
    geometry = GeometrySerializer()

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