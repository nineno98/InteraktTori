from django.shortcuts import render, redirect
from .serializers import TerritorieSerializer, HistorieSerializer, CustomPolygonSerializer, CustomPointSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Territorie, Historie, CustomPolygon, CustomPoint
from rest_framework.views import status
from .forms import LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
# Create your views here.

# Templates

def getMap(request):
    return render(request, 'pages/map.html')

def getLogin(request):
    if request.method == 'POST':
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            messages.add_message(request, messages.SUCCESS, "Sikeres bejelentkezés!")
            return redirect('map')
        
        else:
            form = LoginForm()
            messages.add_message(request, messages.WARNING, "Hibás felhasználónév vagy jelszó!")
            return render(request, 'pages/login.html', {'form':form})
            



    form = LoginForm()
    return render(request, 'pages/login.html', {'form':form })

def getHome(request):
    return render(request,'pages/home.html')

# Rest framework

@api_view(['GET'])
def getTerritories(request):
    territories = Territorie.objects.all()
    serializer = TerritorieSerializer(territories, many = True)
    return Response({
           "success": True,
           "message": "successful get",
           "data": serializer.data
       }, status=status.HTTP_200_OK)

@api_view(['GET'])
def getHistories(request):
    histories = Historie.objects.all()
    serializer = HistorieSerializer(histories, many = True)
    return Response({
           "success": True,
           "message": "successful get",
           "data": serializer.data
       }, status=status.HTTP_200_OK)

@api_view(['GET'])
def getCustomPolygons(request):
    custompol = CustomPolygon.objects.all(filter)
    serializer = CustomPolygonSerializer(custompol, many = True)
    return Response({
           "success": True,
           "message": "successful get",
           "data": serializer.data
       }, status=status.HTTP_200_OK)

@api_view(['GET'])
def getCustompoints(request):
    custompoints = CustomPoint.objects.all()
    serializer = CustomPointSerializer(custompoints, many= True)
    return Response({
           "success": True,
           "message": "successful get",
           "data": serializer.data
       }, status=status.HTTP_200_OK)