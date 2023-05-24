from django.urls import path
from . import views

urlpatterns = [
    path('chor<str:chor_id>/', views.chorhomepage, name='chor-homepage'),
    path('chor<str:chor_id>/songs/', views.chorsongs, name='chor-songs'),
    path('song/<str:pk>/', views.song, name="song"),
    path('create-song/', views.createSong, name="create-song"),
    path('update-song/<str:pk>/', views.updateSong, name="update-song"),
    path('delete-song/<str:pk>/', views.deleteSong, name="delete-song"),
    path('chor<str:chor_id>/performances/', views.chorPerformances, name='chor-performances')
    # path('import-songlist/', views.importSonglist, name='import-songlist'),
    # path('import-performances/', views.importPerformances, name='import-performances'),
]
