from rest_framework.serializers import ModelSerializer
from .models import Territorie, Historie, CustomPolygon, CustomPoint, CustomUser
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