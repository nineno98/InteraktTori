from django.urls import path
from . import views

urlpatterns = [
    path('territories/', view=views.getTerritories, name='getTerritories'),
    path('histories/', view=views.getHistories, name='getHistories'),
    path('custompolygons/', view=views.getCustomPolygons, name='custompolygons'),
    path('custompoints/', view=views.getCustompoints, name='custompoints'),
    path('', view=views.getHome, name='getHome'),
    path('login/', view=views.getLogin, name='login'),
    path('map/', view=views.getMap, name='map'),
]