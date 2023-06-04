from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest


def landingPage(request: WSGIRequest):
    user = request.user
    if user.is_authenticated:
        return redirect('user-page', user.pk)
    context = {}
    return render(request, 'landing.html', context)
