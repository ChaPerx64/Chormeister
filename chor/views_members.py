from .models import Chor, Song, SongPropertyValue, SongPropertyName, SongPerformance
from .forms import SongPropertyNameForm, SongPerformanceForm

from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect

@login_required(login_url='user-login')
def chorMembers(request: WSGIRequest, chor_id):
    chor = Chor.objects.get(id=chor_id)
    members = chor.userchorrole__user_set\
        .filter(chor=chor)\
        .orderby('username')
    context = {
        'chor': chor,
        'members': members,
    }
    return render(request, 'chor/chor-members.html', context)