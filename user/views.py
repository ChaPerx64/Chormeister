from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from chor.models import Chor


''' Authentication pages'''

def loginPage(request):
    page = 'login'
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('user-homepage', user_id=user.pk)
        else:
            messages.error(request, "Username-passord pair is incorrect")
    context = {
        'page': page,
    }
    return render(request, 'user/login-register.html', context)

@login_required(login_url='user-login')
def userHomepage(request, user_id):
    user = User.objects.get(id=user_id)
    chors = Chor.objects.filter(userchorrole__user__pk=user.pk)
    context = {
        'user': user,
        'chors': chors,
    }
    return render(request, 'user/user-homepage.html', context)

@login_required(login_url='user-login')
def logoutUser(request):
    # if request.user.is_authenticated:
    logout(request)
    return redirect('landing')

def registerPage(request):
    page = 'register'
    context = {
        'page': page,
    }
    return render(request, 'user/login-register.html', context)