from .models import Chor
from user.models import User, ChorRole, InviteLink
from cmdjango.settings import CHORMEISTER_DOMAIN
from cmdjango.views import render_chor

from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.handlers.wsgi import WSGIRequest
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404


@login_required(login_url='user-login')
def chorMembers(request: WSGIRequest, chor_id):
    adminrole = ChorRole.get_admin_role()
    chor = get_object_or_404(Chor, id=chor_id)

    # access restriction
    if not chor.user_is_member(request.user.pk):
        messages.error(request, 'Access restricted')
        return redirect('user-homepage')

    members = chor.participants.all()\
        .annotate(chorrole=F('userchorrole__role'))\
        .order_by('-chorrole', 'username')
    try:
        invitelink = f'http://{CHORMEISTER_DOMAIN}/access-invite/?l={InviteLink.objects.get(chor=chor)}'
    except ObjectDoesNotExist:
        invitelink = None
    context = {
        'chor': chor,
        'members': members,
        'adminrole': adminrole.pk,
        'invitelink': invitelink,
        'backlink': '../'
    }
    return render_chor(request, 'chor/chor-members.html', context)


@login_required(login_url='user-login')
def makeMember(request: WSGIRequest, chor_id):
    chor = Chor.objects.get(id=chor_id)
    member = User.objects.get(id=request.GET.get('u'))
    if chor.user_is_admin(request.user) and (not chor.user_is_owner(member)):
        chor.make_member(member)
    return redirect('chor-members', chor_id)


@login_required(login_url='user-login')
def makeAdmin(request: WSGIRequest, chor_id):
    chor = Chor.objects.get(id=chor_id)
    if chor.user_is_admin(request.user):
        member = User.objects.get(id=request.GET.get('u'))
        chor.make_admin(member)
    return redirect('chor-members', chor_id)


@login_required(login_url='user-login')
def kickMember(request: WSGIRequest, chor_id):
    chor = Chor.objects.get(id=chor_id)
    kicker = User.objects.get(id=request.user.pk)
    kickee = User.objects.get(id=request.GET.get('u'))
    if kicker == kickee:
        if not chor.user_is_owner(kickee):
            chor.kick_member(kickee)
            messages.success(request, f'You left {chor.name}')
            return redirect('user-homepage')
    else:
        if chor.user_is_admin(kicker) and (not chor.user_is_owner(kickee)):
            chor.kick_member(kickee)
    return redirect('chor-members', chor_id)
