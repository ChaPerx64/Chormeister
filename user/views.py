# Custom imports
from chor.models import Chor
from .forms import UserCreationForm, UserCreationFormFull
# Django lib imports
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.forms.models import model_to_dict


@login_required(login_url='user-login')
def userHomepage(request: WSGIRequest):
    return redirect('user-page', request.user.pk)


@login_required(login_url='user-login')
def userPage(request: WSGIRequest, user_id: str):
    user = User.objects.get(pk=user_id)
    chors = user.chor_set.all()
    ownerview = True if request.user.pk == user.pk else False
    usr_attribs = dict()
    for key, value in model_to_dict(user).items():
        match key:
            case 'username':
                usr_attribs.update({'Username:': str(value)})
            case 'email':
                usr_attribs.update({'E-mail:': str(value)})
            case 'first_name':
                usr_attribs.update({'First name:': str(value)})
            case 'last_name':
                usr_attribs.update({'Second name:': str(value)})
    context = {
        'user': user,
        'chors': chors,
        'ownerview': ownerview,
        'usr_attribs': usr_attribs,
    }
    return render(request, 'user/user-homepage.html', context)


def loginPage(request: WSGIRequest):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('user-page', user_id=user.pk)
        else:
            messages.error(request, "Username-passord pair is incorrect")
    context = {
        'backlink': '/'
    }
    return render(request, 'user/login-register.html', context)


@login_required(login_url='user-login')
def logoutUser(request: WSGIRequest):
    logout(request)
    return redirect('landing')


# User CRUD pages
def registerPage(request: WSGIRequest):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('user-page', user.pk)
    context = {
        'rendermode': 'register',
        'form': form,
        'backlink': '/'
    }
    return render(request, 'user/login-register.html', context)


@login_required(login_url='user-login')
def editUser(request: WSGIRequest):
    user = User.objects.get(pk=request.user.pk)
    form = UserCreationFormFull(instance=user)
    if request.method == 'POST':
        form = UserCreationFormFull(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('user-page', user.pk)
    context = {
        'form': form,
        'backlink': f'/user/{user.pk}/'
    }
    return render(request, 'user/user-edit.html', context)


@login_required(login_url='user-login')
def deleteUser(request: WSGIRequest):
    user = User.objects.get(pk=request.user.pk)
    if request.method == "POST":
        logout(request)
        user.delete()
        return redirect('landing')
    context = {
        'rendermode': None,
        'obj': user,
        'backlink': f'/user/{user.pk}/'
    }
    return render(request, 'delete.html', context)
