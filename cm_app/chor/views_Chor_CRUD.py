from user.models import User
from .models import Chor
from .forms import ChorForm

from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect


@login_required(login_url='user-login')
def createChor(request: WSGIRequest):
    user = User.objects.get(id=request.user.pk)
    form = ChorForm()
    if request.method == 'POST':
        form = ChorForm(request.POST)
        if form.is_valid():
            chor = form.save(commit=False)
            chor.owner = user
            chor.save()
            chor.make_admin(user)
            return redirect('chor-homepage', chor.pk)
    context = {
        'form': form,
        'chor': None,
        'backlink': '/'
    }
    return render(request, 'chor/chor-form.html', context)


@login_required(login_url='user-login')
def updateChor(request: WSGIRequest, chor_id):
    chor = Chor.objects.get(id=chor_id)
    form = ChorForm(instance=chor)
    if request.method == 'POST':
        form = ChorForm(request.POST, instance=chor)
        if form.is_valid():
            form.save()
            return redirect('chor-homepage', chor.pk)
    context = {
        'form': form,
        'chor': chor,
        'backlink': f'/chor{chor.pk}/'
    }
    return render(request, 'chor/chor-form.html', context)


@login_required(login_url='user-login')
def deleteChor(request: WSGIRequest, chor_id):
    chor = Chor.objects.get(id=chor_id)
    if request.method == "POST":
        chor.delete()
        return redirect('user-homepage')
    context = {
        'obj': chor,
        'backlink': '../'
    }
    return render(request, 'delete.html', context)
