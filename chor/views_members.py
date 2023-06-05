from .models import Chor, Song, SongPropertyValue, SongPropertyName, SongPerformance
from .forms import SongPropertyNameForm, SongPerformanceForm
from user.models import User, ChorRole, UserChorRole

from django.db.models import Count, Q, F
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect


@login_required(login_url='user-login')
def chorMembers(request: WSGIRequest, chor_id):
    adminrole = ChorRole.get_admin_role()
    chor = Chor.objects.get(id=chor_id)
    user = User.objects.get(id=request.user.pk)
    members = chor.participants.all()\
        .annotate(chorrole=F('userchorrole__role'))\
        .order_by('-chorrole', 'username')
    if user.userchorrole_set.get(chor=chor).role == adminrole:
        adminview = True
    else:
        adminview = False
    context = {
        'chor': chor,
        'members': members,
        'adminrole': adminrole.pk,
        'adminview': adminview,
    }
    return render(request, 'chor/chor-members.html', context)
