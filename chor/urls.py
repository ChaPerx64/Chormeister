from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('song/<str:pk>/', views.song, name="song"),
    path('create-song/', views.createSong, name="create-song"),
    path('update-song/<str:pk>/', views.updateSong, name="update-song"),
    path('delete-song/<str:pk>/', views.deleteSong, name="delete-song"),
    path('import-songlist/', views.importSonglist, name='import-songlist'),
    path('import-performances/', views.importPerformances, name='import-performances')
]
