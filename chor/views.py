from django.shortcuts import render, redirect
from django.db.models import Count, Q
from .models import Chor, Song, SongPropertyValue, SongPropertyName, SongPerformance
from .forms import SongPropertyNameForm, SongCreationFormConstructor, SongPerformanceForm
from django.contrib.auth.decorators import login_required


""" General chor views """

@login_required
def chorhomepage(request, chor_id):
    chor = Chor.objects.get(id=chor_id)
    songs = Song.objects.filter(chor=chor_id)
    context = {'songs': songs, 'chor': chor}
    return render(request, 'chor/chor-homepage.html', context)

def chorsongs(request, chor_id):
    chor = Chor.objects.get(id=chor_id)
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
                .annotate(numperformances=Count('songperformance'))
        else:
            songs = chor.song_set.all()\
                .annotate(numperformances=Count('songperformance'))
    attr = SongPropertyName.objects.filter(chor_id=chor_id)
    context = {
        'songs': songs,
        'chor': chor,
        'attributes': attr,
        'sortby': sortby
    }
    return render(request, 'chor/chor-songs.html', context)

def chorPerformances(request, chor_id):
    chor = Chor.objects.get(id=chor_id)
    performances = SongPerformance.objects.filter(song__chor=chor) #.order_by('-datetime')
    out_list = list()
    prev_month = performances[0].dtofperformance.month
    for perf in performances:
        if prev_month != perf.dtofperformance.month:
            out_list.append('')
        out_list.append(perf)
        prev_month = perf.dtofperformance.month
    context = {
        'chor': chor,
        'performances': out_list,
    }
    return render(request, 'chor/chor-performances.html', context)

def chorSongProperties(request, chor_id):
    chor = Chor.objects.get(id=chor_id)
    properties = chor.songpropertyname_set.all()
    context = {
        'chor': chor,
        'properties': properties
    }
    return render(request, 'chor/chor-songproperties.html', context)


""" Song pages """

def song(request, pk):
    song = Song.objects.get(id=pk)
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
        'attributes': attributes,
        'performances':performances
    }
    return render(request, 'chor/song.html', context)

def createSong(request, chor_id):
    chor = Chor.objects.get(id=chor_id)

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
        'chor': chor
    }
    return render(request, 'chor/song_form.html', context)

def updateSong(request, pk):
    song = Song.objects.get(id = pk)
    chor = song.chor

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
                            attr.value = value
                            attr.save()
                            isnew = False
                    if isnew:
                        spn = SongPropertyName.objects.filter(Q(chor=chor) & Q(name=key))[0]
                        SongPropertyValue.objects.create(
                            songpropertyname=spn,
                            song=song,
                            value=value,
                        ).save()
            return redirect('chor-songs', chor_id=chor.pk)

    context = {
        'form': form,
        'chor': chor
    }
    return render(request, 'chor/song_form.html', context)

def deleteSong(request, pk):
    song = Song.objects.get(id=pk)
    chor_id = song.chor.pk
    if request.method == "POST":
        song.delete()
        return redirect('chor-songs', chor_id=chor_id)
    context = {'obj': song}
    return render(request, 'chor/delete.html', context)


""" SongProperty views """

def createProperty(request, chor_id):
    form = SongPropertyNameForm()
    if request.method == "POST":
        form = SongPropertyNameForm(request.POST)
        if form.is_valid():
            songpn = SongPropertyName.objects.create(chor_id=chor_id, name=form.cleaned_data.get('name'))
            songpn.save()
            return redirect('chor-homepage', chor_id=chor_id)
    context = {'form': form}
    return render(request, 'chor/property_form.html', context)

def songPropertyNameDelete(request, prop_id):
    prop = SongPropertyName.objects.get(id=prop_id)
    chor_id = prop.chor.pk
    if request.method == "POST":
        prop.delete()
        return redirect('chor-songproperties', chor_id=chor_id)
    context = {
        'obj': prop
    }
    return render(request, 'chor/delete.html', context)


""" Performance views """

def deletePerformance(request, perf_id):
    perf = SongPerformance.objects.get(id=perf_id)
    chor_id = perf.song.chor.pk
    if request.method == "POST":
        perf.delete()
        return redirect('chor-performances', chor_id=chor_id)
    context = {
        'obj': perf
    }
    return render(request, 'chor/delete.html', context)

def createPerformance(request, song_id):
    song = Song.objects.get(id=song_id)
    form = SongPerformanceForm()
    if request.method == "POST":
        form = SongPerformanceForm(request.POST)
        if form.is_valid():
            songperf = SongPerformance.objects.create(song_id=song_id, dtofperformance=form.cleaned_data.get('dtofperformance'))
            songperf.save()
            return redirect('song', pk=song_id)
    context = {
        'form': form,
        'song': song
    }
    return render(request, 'chor/performance_form.html', context)
