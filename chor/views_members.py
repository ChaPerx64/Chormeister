from .models import Chor, Song, SongPropertyValue, SongPropertyName, SongPerformance
from .forms import SongPropertyNameForm, SongPerformanceForm
from user.models import User, ChorRole, UserChorRole

from django.db.models import Count, Q, F
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect, get_object_or_404


@login_required(login_url='user-login')
def chorMembers(request: WSGIRequest, chor_id):
    adminrole = ChorRole.get_admin_role()
    chor = get_object_or_404(Chor, id=chor_id)
    user = User.objects.get(id=request.user.pk)
    members = chor.participants.all()\
        .annotate(chorrole=F('userchorrole__role'))\
        .order_by('-chorrole', 'username')
    if chor.user_is_admin(user):
        adminview = True
    else:
        adminview = False
    context = {
        'chor': chor,
        'members': members,
        'adminrole': adminrole.pk,
        'adminview': adminview,
        'backlink': '../'
    }
    return render(request, 'chor/chor-members.html', context)


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
    member = User.objects.get(id=request.GET.get('u'))
    if chor.user_is_admin(request.user) and (not chor.user_is_owner(member)):
        chor.kick_member(member)
    return redirect('chor-members', chor_id)