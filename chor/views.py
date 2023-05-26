from django.shortcuts import render, redirect
from django.db.models import Count, Q
from .models import Chor, Song, SongPropertyValue, SongPropertyName, SongPerformance
from .forms import SongForm, SongPropertyNameForm, SongPropertyValueForm, SongCreationFormConstructor


def chorhomepage(request, chor_id):
    chor = Chor.objects.get(id=chor_id)
    songs = Song.objects.filter(chor=chor_id)
    context = {'songs': songs, 'chor': chor}
    return render(request, 'chor/chor-homepage.html', context)

def chorsongs(request, chor_id):
    chor = Chor.objects.get(id=chor_id)
    sortby = request.GET.get('s')
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
                .filter(Q(song__chor__id=chor_id) & Q(songpropertyname__name=sortby))\
                .values("song__id", "song__name", 'value')\
                .order_by(sortq, 'song__name')
            sortby = sortby.capitalize()
    else:
        songs = chor.song_set.all()\
            .annotate(numperformances=Count('songperformance'))\
            .order_by('name')
    attr = SongPropertyName.objects.filter(chor_id=chor_id)
    context = {'songs': songs, 'chor': chor, 'attributes': attr, 'sortby': sortby}
    return render(request, 'chor/chor-songs.html', context)

def song(request, pk):
    song = Song.objects.get(id=pk)
    attributes = song.songpropertyvalue_set.all()
    performances = song.songperformance_set.all()
    context = {'song': song, 'attributes': attributes, 'performances':performances}
    return render(request, 'chor/song.html', context)

def createSong(request, chor_id):
    chor = Chor.objects.get(id=chor_id)

    attrnames = chor.songpropertyname_set.all()
    attrlist = list()
    for attr in attrnames:
        attrlist.append(attr.name)
    
    SongCreationForm = SongCreationFormConstructor(attrlist)
    form = SongCreationForm()

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
                return redirect('chor-homepage', chor_id=chor_id)
    context = {
        'form': form,
    }
    return render(request, 'chor/song_form.html', context)


def updateSong(request, pk):
    song = Song.objects.get(id = pk)
    form = SongForm(instance=song)

    if request.method == "POST":
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            form.save()
            return redirect('chor-homepage')

    context = {'form': form}
    return render(request, 'chor/song_form.html', context)

def deleteSong(request, pk):
    song = Song.objects.get(id=pk)
    chor_id = song.chor.id
    if request.method == "POST":
        song.delete()
        return redirect('chor-songs', chor_id=chor_id)
    context = {'song': song}
    return render(request, 'chor/delete.html', context)

def chorPerformances(request, chor_id):
    chor = Chor.objects.get(id=chor_id)
    performances = SongPerformance.objects.filter(song__chor=chor).order_by('-datetime')
    context = {'chor': chor, 'performances': performances}
    return render(request, 'chor/chor-performances.html', context)