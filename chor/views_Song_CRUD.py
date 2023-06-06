
from cmdjango.views import render_chor
from .models import Chor, Song, SongPropertyValue, SongPropertyName
from .forms import SongCreationFormConstructor

from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect


# Song pages
@login_required(login_url='user-login')
def song(request: WSGIRequest, pk):
    song = Song.objects.get(id=pk)
    chor = song.chor

    # access restriction
    if not chor.user_is_member(request.user.pk):
        messages.error(request, 'You are not a member of the choir')
        return redirect('user-homepage')

    songpropertynames = song.chor.songpropertyname_set.all()

    ''' Initializing attributes dict with empty values of all fields '''
    attributes = dict()
    for name in songpropertynames:
        attributes.update({name.name: ''})
    songpropvalues = song.songpropertyvalue_set.all()

    ''' Filling attributes dict with proopertyvalues from database '''
    for spv in songpropvalues:
        attributes.update({spv.songpropertyname.name: spv.value})

    ''' Finding performances of the song '''
    performances = song.songperformance_set.all()

    ''' Putting out '''
    context = {
        'song': song,
        'chor': chor,
        'attributes': attributes,
        'performances': performances,
        'backlink': f'/chor{song.chor.pk}/songs/',
    }
    return render_chor(request, 'chor/song.html', context)


@login_required(login_url='user-login')
def createSong(request: WSGIRequest, chor_id):
    chor = Chor.objects.get(id=chor_id)

    # access restriction
    if not chor.user_is_admin(request.user.pk):
        messages.error(request, 'Admin level access needed')
        return redirect('chor-songs', chor.pk)

    ''' Creating fields list for a custom form '''
    attrnames = chor.songpropertyname_set.all()
    attrlist = list()
    for attr in attrnames:
        attrlist.append(attr.name)

    ''' Creating Form Class dynamically with custom constructor '''
    SongCreationForm = SongCreationFormConstructor(attrlist)
    form = SongCreationForm()

    ''' Logic for dealing with saving of the created data '''
    if request.method == "POST":
        form = SongCreationForm(request.POST)
        if form.is_valid():
            song = Song.objects.create(
                chor_id=chor_id,
                name=form.cleaned_data.get('name')
            )
            new_attr_values = list()
            for attr in attrnames:
                new_value = form.cleaned_data.get(attr.name)
                if new_value:
                    spv = SongPropertyValue.objects.create(
                        songpropertyname=attr,
                        song=song,
                        value=new_value,
                    )
                    new_attr_values.append(spv)
            if song:
                song.save()
                for val in new_attr_values:
                    val.save()
                return redirect('chor-songs', chor_id=chor_id)
    context = {
        'form': form,
        'chor': chor,
        'song': None,
        'backlink': f'/chor{chor.pk}/songs/'
    }
    return render(request, 'chor/song_form.html', context)


@login_required(login_url='user-login')
def updateSong(request: WSGIRequest, pk):
    song = Song.objects.get(id=pk)
    chor = song.chor

    # access restriction
    if not chor.user_is_admin(request.user.pk):
        messages.error(request, 'Admin level access needed')
        return redirect('song', song.pk)

    ''' Creating fields list for a custom form '''
    attrnames = chor.songpropertyname_set.all()
    attrlist = list()
    for attr in attrnames:
        attrlist.append(attr.name)

    ''' Gathering initial data for the form '''
    initialdata = {'name': song.name}
    songattribs = song.songpropertyvalue_set.all()
    for item in songattribs:
        initialdata.update({item.songpropertyname.name: item.value})

    ''' Creating Form Class dynamically with custom constructor '''
    SongCreationForm = SongCreationFormConstructor(attrlist)
    form = SongCreationForm(initial=initialdata)

    ''' Logic for dealing with saving changes '''
    if request.method == "POST":
        form = SongCreationForm(request.POST)
        if form.is_valid():
            for key, value in form.cleaned_data.items():
                if key == 'name':
                    song.name = value
                    song.save()
                else:
                    isnew = True
                    for attr in songattribs:
                        if key == attr.songpropertyname.name:
                            if value != '':
                                attr.value = value
                                attr.save()
                            else:
                                attr.delete()
                            isnew = False
                    if isnew & (value != ''):
                        spn = SongPropertyName.objects.filter(
                            Q(chor=chor) & Q(name=key))[0]
                        SongPropertyValue.objects.create(
                            songpropertyname=spn,
                            song=song,
                            value=value,
                        ).save()
            return redirect('chor-songs', chor_id=chor.pk)

    context = {
        'form': form,
        'chor': chor,
        'song': song,
        'backlink': f'/song/{song.pk}/'
    }
    return render(request, 'chor/song_form.html', context)


@login_required(login_url='user-login')
def deleteSong(request: WSGIRequest, pk):
    song = Song.objects.get(id=pk)
    chor = song.chor

    # access restriction
    if not chor.user_is_admin(request.user.pk):
        messages.error(request, 'Admin level access needed')
        return redirect('song', song.pk)

    if request.method == "POST":
        song.delete()
        return redirect('chor-songs', chor_id=chor.pk)
    context = {
        'obj': song,
        'backlink': f'/song/{song.pk}/',
    }
    return render(request, 'delete.html', context)
