from django.shortcuts import render
from .serializers import TerritorieSerializer, HistorieSerializer, CustomPolygonSerializer, CustomPointSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Territorie, Historie, CustomPolygon, CustomPoint
# Create your views here.

# Rest framework
@api_view(['GET'])
def getTerritories(request):
    territories = Territorie.objects.all()
    serializer = TerritorieSerializer(territories, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getHistories(request):
    histories = Historie.objects.all()
    serializer = HistorieSerializer(histories, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getCustomPolygons(request):
    custompol = CustomPolygon.objects.all()
    serializer = CustomPolygonSerializer(custompol, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getCustompoints(request):
    custompoints = CustomPoint.objects.all()
    serializer = CustomPointSerializer(custompoints, many= True)
    return Response(serializer.data)