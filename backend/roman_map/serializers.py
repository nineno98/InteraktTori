from rest_framework.serializers import ModelSerializer
from .models import Territorie, Historie, CustomPolygon, CustomPoint
from rest_framework import serializers
import json
import geojson


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
            properties = {
                "id": instance.id,
                "name": instance.name,
                "description": instance.description,
                "created_by": instance.created_by
                
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
            properties = {
                "id": instance.id,
                "name": instance.name,
                "description": instance.description,
                "created_by": instance.created_by
            }
            feature = geojson.Feature(properties=properties, geometry=point)

        except json.JSONDecodeError as e:
            raise serializers.ValidationError("Hibás JSON formátum. "+str(e))
        except Exception as e:
            raise serializers.ValidationError("Hiba. "+str(e))
        return feature