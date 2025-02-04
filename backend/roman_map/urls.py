from django.urls import path
from . import views

urlpatterns = [
    path('territories/', view=views.getTerritories, name='getTerritories'),
    path('histories/', view=views.getHistories, name='getHistories'),
    path('', view=views.fooldal, name='fooldal'),
    path('login/', view=views.bejelentkezes, name='bejelentkezes'),
    path('map/', view=views.terkep, name='terkep'),
    path('logout/', view=views.kijelentkezes, name='kijelentkezes'),
    path('password/', view=views.jelszovaltas, name='jelszovaltas'),
    path('user-infos/', view=views.sajatadatok, name='sajatadatok'),
    path('custom-draws/', view=views.customDraws, name='customDraws'),
    path('test/', views.teszt, name='teszt'),
    path('test/add-test/', view=views.uj_teszt_keszitese, name='uj_teszt_keszitese'),
    path('test/<int:quiz_id>/test-details/', view=views.teszt_reszletei, name='teszt_reszletei'),
    path("test/<int:quiz_id>/add-question/<str:question_type>/", view=views.kerdes_hozzadasa, name="kerdes_hozzadasa"),
    path('test/<int:quiz_id>/delete/', view=views.teszt_torlese, name='teszt_torlese'),
    path('test/<int:quiz_id>/test-details/<int:question_id>/', view=views.kerdes_torlese, name='kerdes_torlese'),
    path('test/run-test/<int:quiz_id>/', view=views.teszt_inditasa, name='teszt_inditasa'),

]