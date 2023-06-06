from django.urls import path
from . import views

urlpatterns = [
    # General chor pages
    path('chor<str:chor_id>/', views.chorhomepage, name='chor-homepage'),
    path('chor<str:chor_id>/songs/', views.chorsongs, name='chor-songs'),
    path('chor<str:chor_id>/performances/',
         views.chorPerformances, name='chor-performances'),
    path('chor<str:chor_id>/songproperties/',
         views.chorSongProperties, name="chor-songproperties"),

    # Chor CRUD ops
    path('create-chor/', views.createChor, name='create-chor'),
    path('chor<str:chor_id>/edit-info/', views.updateChor, name='update-chor'),
    path('chor<str:chor_id>/delete/', views.deleteChor, name='delete-chor'),

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

    # members pages
    path('chor<str:chor_id>/members/', views.chorMembers, name='chor-members'),
    path('chor<str:chor_id>/make-member/', views.makeMember, name='chor-make-member'),
    path('chor<str:chor_id>/kick-member/', views.kickMember, name='chor-kick-member'),
    path('chor<str:chor_id>/make-admin/', views.makeAdmin, name='chor-make-admin'),

    # InviteLink views
    path('chor<str:chor_id>/create-invite/', views.createInviteLink, name='chor-create-invite'),
    path('access-invite/', views.inviteLinkAccessed, name='access-invite'),
]
