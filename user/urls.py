from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='user-login'),
    path('logout/', views.logoutUser, name='user-logout'),
    path('register/', views.registerPage, name='user-register'),
    path('<str:user_id>/', views.userHomepage, name='user-homepage'),
]