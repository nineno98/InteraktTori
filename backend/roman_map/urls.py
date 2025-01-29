from django.urls import path
from . import views

urlpatterns = [
    path('territories/', view=views.getTerritories, name='getTerritories'),
    path('histories/', view=views.getHistories, name='getHistories'),
    path('custompolygons/', view=views.getCustomPolygons, name='custompolygons'),
    path('custompoints/', view=views.getCustompoints, name='custompoints'),
    path('', view=views.fooldal, name='fooldal'),
    path('login/', view=views.bejelentkezes, name='bejelentkezes'),
    path('map/', view=views.terkep, name='terkep'),
    path('logout/', view=views.kijelentkezes, name='kijelentkezes'),
    path('password/', view=views.jelszovaltas, name='jelszovaltas'),
    path('user-infos/', view=views.sajatadatok, name='sajatadatok'),
    path('custom-draws/', view=views.customDraws, name='customDraws'),
]