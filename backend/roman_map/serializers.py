from rest_framework.serializers import ModelSerializer
from .models import Territorie, Historie, CustomUser, CustomDraw, AncientPlaces, Question, UserAnswer
from rest_framework import serializers
import json
import geojson


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name']

class AncientPlacesSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        
        try:
            geometry = json.loads(instance.coordinates)
            multipolygon = geojson.Point(geometry)
            properties = {
                "id": instance.id,
                "ancient_name": instance.ancient_name,
                "modern_name": instance.modern_name
            }
            feature = geojson.Feature(properties=properties, geometry=multipolygon)
        
        except json.JSONDecodeError as e:
            raise serializers.ValidationError("Hibás JSON formátum. "+str(e))
        except Exception as e:
            raise serializers.ValidationError("Hiba. "+str(e))
        return feature

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
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Historie
        fields = ['id', 'name', 'description', 'historie_type', 'image_url', 'date', 'points']

    def get_image_url(self, obj):
        try:
            request = self.context.get('request')   
            if obj.image and request:
                return request.build_absolute_uri(obj.image.url)
            return None
        except Exception as e:
            raise serializers.ValidationError("Hiba a kép url lekérése során.")
    def to_representation(self, instance):
        try:
            geometry = json.loads(instance.coordinates)
            multipoint = geojson.MultiPoint(geometry)
            properties = {
                "id": instance.id,
                "name": instance.name,
                "description": instance.description,
                "date":instance.date,
                "image_url":self.get_image_url(instance)    
            }
            feature = geojson.Feature(properties=properties, geometry=multipoint)
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
        try:
            return CustomDraw.objects.create(**validated_data)
        except Exception as e:
            raise serializers.ValidationError(f"Hiba az objektum mentése során.{e}")

    def update(self, instance, validated_data):
        try:
            coordinates = validated_data.get('coordinates')
            instance.coordinates = coordinates
            instance.save()
            return instance
        except Exception as e:
            raise serializers.ValidationError(f"Hiba a objektum frissítése közben. {e}")
    
    def to_internal_value(self, data):
        try:
            request = self.context.get("request", None)
            if request is None:
                raise serializers.ValidationError({"request": "A kérés nem érhető el a serializer contextjében."})
            if request.method == 'POST':
                if not isinstance(data, dict):
                    raise serializers.ValidationError({"geojson": "A megadott adat nem érvényes JSON objektum."})
                if data.get("type") != "Feature":
                    raise serializers.ValidationError({"geojson": "A 'type' mező értékének 'Feature'-nek kell lennie."})
                properties = data.get("properties", {})
                geometry = data.get("geometry", {})
                if "coordinates" not in geometry or "type" not in geometry:
                    raise serializers.ValidationError({"geometry": "A 'geometry' mező hibás vagy hiányzik."})
                user = CustomUser.objects.get(id=properties["created_by"])
                if not user:
                    raise serializers.ValidationError({"created_by": "A megadott felhasználó nem létezik."})               
                return {
                    "name": properties.get("name", ""),
                    "description": properties.get("description", ""),
                    "created_by": user,
                    "coordinates": json.dumps(geometry["coordinates"]),
                    "type": geometry["type"].lower(),
                }
            elif request.method == 'PATCH':
                if "coordinates" not in data:
                    raise serializers.ValidationError({"coordinates": "Ez a mező kötelező frissítéskor."})
                elif not isinstance(data["coordinates"], (list, tuple)):
                    raise serializers.ValidationError({"coordinates": "A koordinátáknak listának kell lenniük."})
                return {"coordinates": json.dumps(data["coordinates"])}
            else:
                raise serializers.ValidationError("Hiba: nem támogatott HTTP metódus.")
        except Exception as e:
            raise serializers.ValidationError(f"Hiba az objektum előkészítése során. {e}")
       
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
            raise serializers.ValidationError(f"Hibás JSON formátum. {e}")
        except Exception as e:
            raise serializers.ValidationError(f"Hiba a reprezentáció során: {e}")
        return feature
    
class QuestionSerializer(serializers.ModelSerializer):
    #correct_answers = serializers.SerializerMethodField()
    score_ratio = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ['id', 'text', 'score_ratio']
    
    def get_score_ratio(self, obj):
        return float(getattr(obj, 'score_ratio', None))