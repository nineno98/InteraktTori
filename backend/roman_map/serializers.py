from rest_framework.serializers import ModelSerializer
from .models import Territorie, Historie, CustomPolygon, CustomPoint
from rest_framework import serializers

class TerritorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Territorie
        fields = '__all__'

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