
from cmdjango.views import render_chor
from .models import Chor, Song, SongPropertyValue, SongPropertyName, SongPerformance
from .forms import SongPropertyNameForm, SongPerformanceForm

from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect, get_object_or_404

from .views_Chor_CRUD import createChor, deleteChor, updateChor
from .views_Song_CRUD import song, createSong, deleteSong, updateSong
from .views_members import chorMembers, kickMember, makeAdmin, makeMember
from .views_InviteLinks import createInviteLink, inviteLinkAccessed

# General chor views


@login_required(login_url='user-login')
def chorhomepage(request: WSGIRequest, chor_id):
    chor = get_object_or_404(Chor, id=chor_id)

    # access restriction
    if not chor.user_is_member(request.user.pk):
        messages.error(request, 'You are not a member of the choir')
        return redirect('user-homepage')

    context = {
        'chor': chor,
        'backlink': '/',
    }
    return render_chor(request, 'chor/chor-homepage.html', context)


@login_required(login_url='user-login')
def chorsongs(request: WSGIRequest, chor_id):
    chor = Chor.objects.get(id=chor_id)

    # access restriction
    if not chor.user_is_member(request.user.pk):
        messages.error(request, 'You are not a member of the choir')
        return redirect('user-homepage')

    sortby = request.GET.get('s')
    qstr = request.GET.get('q')
    if sortby:
        if 'numperformances' in sortby:
            songs = chor.song_set.all()\
                .annotate(numperformances=Count('songperformance'))\
                .order_by(sortby)
            sortby = None
        else:
            if sortby[0] == '-':
                sortq = '-value'
                sortby = sortby.lstrip('-')
            else:
                sortq = 'value'
            songs = SongPropertyValue.objects\
                .filter(
                    Q(song__chor__id=chor_id) &
                    Q(songpropertyname__name=sortby)
                )\
                .values("song__id", "song__name", 'value')\
                .order_by(sortq, 'song__name')
            sortby = sortby.capitalize()
    else:
        if qstr:
            songs = chor.song_set.filter(
                Q(name__icontains=qstr) |
                Q(songpropertyvalue__value__icontains=qstr)
            )\
                .annotate(numperformances=Count('songperformance'))\
                .order_by('name')
        else:
            songs = chor.song_set.all()\
                .annotate(numperformances=Count('songperformance'))\
                .order_by('name')
    attr = SongPropertyName.objects.filter(chor_id=chor_id)
    context = {
        'songs': songs,
        'chor': chor,
        'attributes': attr,
        'sortby': sortby,
        'qstr': qstr,
        'backlink': "../"
    }
    return render_chor(request, 'chor/chor-songs.html', context)


@login_required(login_url='user-login')
def chorPerformances(request: WSGIRequest, chor_id):
    chor = Chor.objects.get(id=chor_id)

    # access restriction
    if not chor.user_is_member(request.user.pk):
        messages.error(request, 'You are not a member of the choir')
        return redirect('user-homepage')

    performances = SongPerformance.objects.filter(song__chor=chor)
    out_list = list()
    if len(performances):
        prev_month = performances[0].dtofperformance.month
        for perf in performances:
            if prev_month != perf.dtofperformance.month:
                out_list.append('')
            out_list.append(perf)
            prev_month = perf.dtofperformance.month
    context = {
        'chor': chor,
        'performances': out_list,
        'backlink': '../',
    }
    return render_chor(request, 'chor/chor-performances.html', context)


@login_required(login_url='user-login')
def chorSongProperties(request: WSGIRequest, chor_id):
    chor = Chor.objects.get(id=chor_id)

    # access restriction
    if not chor.user_is_member(request.user.pk):
        messages.error(request, 'You are not a member of the choir')
        return redirect('user-homepage')

    properties = chor.songpropertyname_set.all()

    context = {
        'chor': chor,
        'properties': properties,
        'backlink': f'/chor{chor.pk}/songs/',
    }
    return render_chor(request, 'chor/chor-songproperties.html', context)


# SongProperty views
@login_required(login_url='user-login')
def createProperty(request: WSGIRequest, chor_id):

    # access restriction
    chor = Chor.objects.get(id=chor_id)
    if not chor.user_is_admin(request.user.pk):
        messages.error(request, 'Admin level access needed')
        return redirect('chor-songs', chor.pk)

    form = SongPropertyNameForm()
    if request.method == "POST":
        form = SongPropertyNameForm(request.POST)
        if form.is_valid():
            songpn = SongPropertyName.objects.create(
                chor_id=chor_id, name=form.cleaned_data.get('name'))
            songpn.save()
            return redirect('chor-homepage', chor_id=chor_id)
    context = {
        'form': form,
    }
    return render(request, 'chor/property_form.html', context)


@login_required(login_url='user-login')
def songPropertyNameDelete(request: WSGIRequest, prop_id):
    prop = SongPropertyName.objects.get(id=prop_id)
    chor = prop.chor

    # access restriction
    if not prop.chor.user_is_admin(request.user.pk):
        messages.error(request, 'Admin level access needed')
        return redirect('chor-properties', chor.pk)

    if request.method == "POST":
        prop.delete()
        return redirect('chor-songproperties', chor_id=chor.pk)
    context = {
        'obj': prop,
    }
    return render(request, 'delete.html', context)


# Performance views """
@login_required(login_url='user-login')
def deletePerformance(request: WSGIRequest, perf_id):
    perf = SongPerformance.objects.get(id=perf_id)
    chor = perf.song.chor

    # access restriction
    if not chor.user_is_admin(request.user.pk):
        messages.error(request, 'Admin level access needed')
        return redirect('song', perf.song.pk)

    if request.method == "POST":
        perf.delete()
        return redirect('chor-performances', chor_id=chor.pk)
    context = {
        'obj': perf,
        'backlink': f'/song/{perf.song.pk}'
    }
    return render(request, 'delete.html', context)


@login_required(login_url='user-login')
def createPerformance(request: WSGIRequest, song_id):
    song = Song.objects.get(id=song_id)

    # access restriction
    if not song.chor.user_is_admin(request.user.pk):
        messages.error(request, 'Admin level access needed')
        return redirect('song', song.pk)

    form = SongPerformanceForm()
    if request.method == "POST":
        form = SongPerformanceForm(request.POST)
        if form.is_valid():
            songperf = SongPerformance.objects.create(
                song_id=song_id, dtofperformance=form.cleaned_data.get('dtofperformance'))
            songperf.save()
            return redirect('song', pk=song_id)
    context = {
        'form': form,
        'song': song,
    }
    return render(request, 'chor/performance_form.html', context)
