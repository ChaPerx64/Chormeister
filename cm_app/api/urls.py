from django.urls import path
from . import views

urlpatterns = [
    path('getchorsongs/', views.getChorSongsJson, name='getchorsongs'),
    path('getchorperformances/', views.getChorPerformancesJson, name='getchorperformances'),
]