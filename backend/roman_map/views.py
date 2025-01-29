from django.shortcuts import render, redirect
from .serializers import TerritorieSerializer, HistorieSerializer, CustomPolygonSerializer, CustomPointSerializer, CustomDrawSerializer, CustomDrawSerializer_
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Territorie, Historie, CustomPolygon, CustomPoint, CustomDraw
from rest_framework.views import status
from .forms import LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import geojson
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

# Templates

def sajatadatok(request):
    return render(request, 'pages/user_informations.html')

def jelszovaltas(request):
    try:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, "A jelszó sikeresen módosítva! ")
                return redirect('fooldal')
            else:
                messages.error(request, "Hiba: A jelszó módosítása sikertelen!")
        else:
            form = PasswordChangeForm(request.user)
            print(form.errors)
        return render(request, 'accounts/change_password.html', {'form':form})
    except Exception as e:
        print(str(e))

def terkep(request):
    return render(request, 'pages/map.html')

def kijelentkezes(request):
    try:
        logout(request)
        return redirect('fooldal')
    except Exception as e:
        print(str(e))


def bejelentkezes(request):
    try:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Sikeres bejelentkezés")
                    return redirect('fooldal')
            
                else:
                    form = LoginForm()
                    messages.warning(request, "Sikertelen bejelentkezés. Hibás felhsználónév vagy jelszó")
                    return render(request, 'pages/login.html', {'form':form, 'message':'Sikertelen bejelentkezés. Hibás felhasználónév vagy jelszó!'})
            else:
                messages.error(request, "Hiba a belépés során! Ellenőrizze a felhasználónevet és jelszót!")
                return render(request, 'pages/login.html', {'form':form})
        form = LoginForm()
        return render(request, 'pages/login.html', {'form':form })
    except Exception as e:
        pass

def fooldal(request):
    return render(request,'pages/home.html')

# Rest framework

@api_view(['GET'])
def getTerritories(request):
    territories = Territorie.objects.all()
    serializer = TerritorieSerializer(territories, many = True)
    geojson_data = geojson.FeatureCollection(features=serializer.data)
    return JsonResponse(geojson_data)

@api_view(['GET'])
def getHistories(request):
    histories = Historie.objects.all()
    serializer = HistorieSerializer(histories, many=True)
    geojson_data = geojson.FeatureCollection(features=serializer.data)
    return JsonResponse(geojson_data)

@api_view(['GET'])
def getCustomPolygons(request):
    custompolygons = CustomPolygon.objects.all()
    serializer = CustomPolygonSerializer(custompolygons, many=True)
    geojson_data = geojson.FeatureCollection(features=serializer.data)
    return JsonResponse(geojson_data)

@api_view(['GET'])
def getCustompoints(request):
    custompoints = CustomPoint.objects.all()
    serializer = CustomPointSerializer(custompoints, many= True)
    return Response({
           "success": True,
           "message": "successful get",
           "data": serializer.data
       }, status=status.HTTP_200_OK)

#@permission_classes([IsAuthenticated])
@api_view(['GET','POST', 'PATCH'])
@csrf_exempt
def customDraws(request):
    if request.method == 'GET':
        customdraws = CustomDraw.objects.filter(created_by=request.user)
        serializer = CustomDrawSerializer(customdraws, many= True)
        geojson_data = geojson.FeatureCollection(features=serializer.data)
        return JsonResponse(geojson_data)
    elif request.method == 'POST':
        serializer = CustomDrawSerializer_(data=request.data)
        if serializer.is_valid():
            new_draw = serializer.save()
            response = {
                "status":"success",
                "object_id": new_draw.id
            }
            return JsonResponse(response, status = 200)
        else:
            response = {
                "status":"error",
                "message":serializer.errors
            }
            return JsonResponse(response, status = 400)
    elif request.method == 'PATCH':
        print(f"Beérkezett adatok: {request.data}")
        obj_id = request.data.pop('id')
        print(f"Beérkezett adatok: {request.data}")
        coordinates_str = json.dumps(request.data['coordinates'])
        request.data['coordinates'] = coordinates_str
        print(f"Beérkezett adatok2: {request.data}")

        try:
            custom_draw = CustomDraw.objects.get(id = obj_id)
        except CustomDraw.DoesNotExist:
            response = {
                "status":"error",
                "message":"A módosítani kívánt elem nem található az adatbázisban."
            }
            return JsonResponse(response, status=404)
        serializer = CustomDrawSerializer_(custom_draw, data=request.data, partial = True)
        
        if serializer.is_valid(raise_exception=True):
            print(f"Validált adatok: {serializer.validated_data}")
            serializer.save()
            response = {
                "status":"success",
                "message":"Az elem módosítása sikeresen megtörtént."
            }
            return JsonResponse(response, status= 200)

