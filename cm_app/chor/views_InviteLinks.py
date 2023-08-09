# Custom imports
from user.models import InviteLink
from .models import Chor
# Django lib imports
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.contrib import messages


# InviteLink CRUD
@login_required(login_url='user-login')
def createInviteLink(request: WSGIRequest, chor_id):
    chor = get_object_or_404(Chor, id=chor_id)

    # access restriction
    if not chor.user_is_admin(request.user.pk):
        messages.error(request, 'Admin level access needed')
        return redirect('chor-homepage', chor.pk)

    if chor.user_is_admin(request.user):
        created = False
        while not created:
            invite, created = InviteLink.objects.get_or_create(chor=chor)
            if created:
                invite.save()
            else:
                invite.delete()
    return redirect('chor-members', chor.id)


@login_required(login_url='user-login')
def inviteLinkAccessed(request: WSGIRequest):
    invite = get_object_or_404(InviteLink, id=request.GET.get('l'))
    chor = invite.chor
    chor.make_member(request.user)
    messages.success(request, f'Use are now part of {chor.name}')
    return redirect('chor-homepage', chor.id)
