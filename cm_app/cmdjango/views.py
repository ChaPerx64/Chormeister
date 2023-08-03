from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, get_object_or_404
from chor.models import Chor


def landingPage(request: WSGIRequest):
    user = request.user
    if user.is_authenticated:
        return redirect('user-page', user.pk)
    context = {}
    return render(request, 'landing.html', context)


def render_chor(request, template_name, context=None, content_type=None, status=None, using=None):
    if context:
        chor = context.get('chor')
        if chor:
            chor = get_object_or_404(Chor, id=chor.id)
            adminview = False
            if chor.user_is_admin(request.user):
                adminview = True
            context.update({'adminview': adminview})
    return render(request, template_name, context=context, content_type=content_type, status=status, using=using)
