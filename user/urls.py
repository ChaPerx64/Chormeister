from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginPage, name='user-login'),
    path('logout/', views.logoutUser, name='user-logout'),
    path('register/', views.registerPage, name='user-register'),
    path('user/<str:user_id>/', views.userPage, name='user-page'),
    path('user-homepage/', views.userHomepage, name='user-homepage'),
    path('user-edit/', views.editUser, name='user-edit'),
    path('user-delete/', views.deleteUser, name='user-delete'),
]
