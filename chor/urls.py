from django.urls import path
from . import views

urlpatterns = [
    # General chor pages
    path('chor<str:chor_id>/', views.chorhomepage, name='chor-homepage'),
    path('create-chor/', views.createChor, name='create-chor'),
    path('edit-chor/<str:chor_id>/', views.editChor, name='edit-chor'),
    path('chor<str:chor_id>/songs/', views.chorsongs, name='chor-songs'),
    path('chor<str:chor_id>/performances/',
         views.chorPerformances, name='chor-performances'),
    path('chor<str:chor_id>/songproperties/',
         views.chorSongProperties, name="chor-songproperties"),

    # Song pages
    path('song/<str:pk>/', views.song, name="song"),
    path('chor<str:chor_id>/create-song/',
         views.createSong, name="create-song"),
    path('update-song/<str:pk>/', views.updateSong, name="update-song"),
    path('delete-song/<str:pk>/', views.deleteSong, name="delete-song"),

    # SongProperty pages
    path('chor<str:chor_id>/create-property/',
         views.createProperty, name="create-property"),
    path('propertyname<str:prop_id>/delete/',
         views.songPropertyNameDelete, name="songpropertyname-delete"),

    # Performance pages
    path('song/<str:song_id>/create-performance/',
         views.createPerformance, name='create-performance'),
    path('deletePerformance/<str:perf_id>/',
         views.deletePerformance, name='delete-performance'),
]
