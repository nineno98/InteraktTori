from django.shortcuts import render, redirect, get_object_or_404
from .serializers import TerritorieSerializer, HistorieSerializer, CustomDrawSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Territorie, Historie, CustomDraw, Quiz
from rest_framework.views import status
from .forms import LoginForm, QuizForm, QuestionTypeForm, QuestionForm, ValaszelemForm,IgazHamisForm
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
    serializer = HistorieSerializer(histories, many = True, context={'request': request})
    geojson_data = geojson.FeatureCollection(features=serializer.data)
    return JsonResponse(geojson_data, safe=False)


@permission_classes([IsAuthenticated])
@api_view(['GET','POST', 'PATCH', 'DELETE'])
@csrf_exempt
def customDraws(request):
    if request.method == 'GET':
        customdraws = CustomDraw.objects.filter(created_by=request.user)
        serializer = CustomDrawSerializer(customdraws, many= True)
        geojson_data = geojson.FeatureCollection(features=serializer.data)
        return JsonResponse(geojson_data)
    elif request.method == 'POST':
        serializer = CustomDrawSerializer(data=request.data, context={"request": request})
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
        obj_id = request.data.pop('id')
        try:
            custom_draw = CustomDraw.objects.get(id = obj_id)
        except CustomDraw.DoesNotExist:
            response = {
                "status":"error",
                "message":"A módosítani kívánt elem nem található az adatbázisban."
            }
            return JsonResponse(response, status=404)
        serializer = CustomDrawSerializer(custom_draw, data=request.data, partial = True, context={"request": request})
        
        if serializer.is_valid(raise_exception=True):
            print(f"Validált adatok: {serializer.validated_data}")
            serializer.save()
            response = {
                "status":"success",
                "message":"Az elem módosítása sikeresen megtörtént."
            }
            return JsonResponse(response, status= 200)
    elif request.method == 'DELETE':
        remowend_id = request.data.get('id')
        try:
            obj = CustomDraw.objects.get(id=remowend_id)
            obj.delete()
            response = {
                "status":"success",
                "message":"Az elem törlése sikeresen megtörtént."
            }
            return JsonResponse(response, status=200)
        except CustomDraw.DoesNotExist:
            response = {
                "status":"error",
                "message":"Az elem törlése sikertelen. Az elem nem található."
            }
            return JsonResponse(response, status=404)

def teszt(request):
    all_quizs = Quiz.objects.all()
    return render(request,'pages/test.html',{"quiz_list":all_quizs})

def uj_teszt_keszitese(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.created_by = request.user
            form.save()
            return redirect('teszt_reszletei', quiz_id=quiz.id)
        else:
            messages.error(request, "Hiba történt, a teszt létrehozása sikertelen!")
    else:
        form = QuizForm()
        return render(request, 'pages/create_test.html', {"form":form})

def teszt_reszletei(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id = quiz_id)
    except Quiz.DoesNotExist:
        messages.error(request, "Hiba történt a folyamat során!")
    if request.method == "POST":
        form = QuestionTypeForm(request.POST)
        if form.is_valid():
            question_type = form.cleaned_data["question_type"]
            return redirect("kerdes_hozzadasa", quiz_id=quiz.id, question_type=question_type)
    

    questions = quiz.questions.all()  # Meglévő kérdések listája
    form = QuestionTypeForm()
    return render(request, "pages/test_details.html", {
        "quiz": quiz,
        "questions": questions,
        "form": form
    })

def kerdes_hozzadasa(request, quiz_id, question_type):
    try:
        quiz = Quiz.objects.get(id = quiz_id)
    except Quiz.DoesNotExist:
        messages.error(request, "Hiba történt a folyamat során!")
    if question_type == "mc":  # Több válaszos
        AnswerFormSetClass = ValaszelemForm
    else:  # Igaz/Hamis
        AnswerFormSetClass = IgazHamisForm

    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        formset = AnswerFormSetClass(request.POST)

        if question_form.is_valid() and formset.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.question_type = question_type
            question.save()

            answers = formset.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()

            return redirect("teszt_reszletei", quiz_id=quiz.id)  # Tovább a kvízhez

    else:
        question_form = QuestionForm()
        formset = AnswerFormSetClass()

    return render(request, "pages/create_question.html", {
        "quiz": quiz,
        "question_form": question_form,
        "formset": formset,
        "question_type": question_type
    })

