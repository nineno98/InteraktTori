from rest_framework.serializers import ModelSerializer
from .models import Territorie, Historie, CustomPolygon, CustomPoint
from rest_framework import serializers
import json

class CoordinatesConvert(serializers.Field):
    def to_representation(self, value):
        try:
            return json.loads(value)
        except:
            raise serializers.ValidationError("Serializer hiba: A JSON formátum nem valid.")
    
    def to_internal_value(self, data):
        try:
            return json.dump(data)
        except:
            raise serializers.ValidationError("Serializer hiba: A JSON formátum nem valid.")


class TerritorieSerializer(serializers.ModelSerializer):
    coordinates = CoordinatesConvert()
    class Meta:
        model = Territorie
        fields = ['id', 'name', 'start_date', 'end_date', 'color', 'coordinates']

class HistorieSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Historie
        fields = '__all__'

class CustomPolygonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomPolygon
        fields = '__all__'

class CustomPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomPoint
        fields = '__all__'