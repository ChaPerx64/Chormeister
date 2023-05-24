# from .cmbot_songs import SongList
# from .cmbot_performances import PerformanceList
from django.shortcuts import render, redirect
from django.db.models import Count
from .models import Chor, Song, SongPropertyValue, SongPropertyName, SongPerformance
from .forms import SongForm, SongPropertyNameForm, SongPropertyValueForm
import datetime


def chorhomepage(request, chor_id):
    chor = Chor.objects.get(id=chor_id)
    songs = Song.objects.filter(chor=chor_id)
    context = {'songs': songs, 'chor': chor}
    return render(request, 'chor/chor-homepage.html', context)

def chorsongs(request, chor_id):
    chor = Chor.objects.get(id=chor_id)
    songs = Song.objects.filter(chor_id=chor_id).annotate(numperformances=Count('songperformance')).order_by('-numperformances')
    context = {'songs': songs, 'chor': chor}
    return render(request, 'chor/chor-songs.html', context)

def song(request, pk):
    song = Song.objects.get(id=pk)
    attributes = SongPropertyValue.objects.filter(song_id=pk)
    performances = SongPerformance.objects.filter(song_id=pk)
    context = {'song': song, 'attributes': attributes, 'performances':performances}
    return render(request, 'chor/song.html', context)

def createSong(request):
    form = SongForm()

    if request.method == "POST":
        form = SongForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chor-homepage')
    
    context = {'form': form}
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
    if request.method == "POST":
        song.delete()
        return redirect('home')
    context = {'obj': song}
    return render(request, 'chor/delete.html', context)

# def importSonglist(request):
#     sl = SongList('chor/songlist.json').json_ready()
    
#     out_list = list()
#     context = dict()
    
#     for songo in sl.values():
#         if songo['status'] != 'deleted':
#             song_match = Song.objects.get(name=songo['name'])
#             for key, value in songo.items():
#                 if not key in ('status', 'name'):
#                     value_match = SongPropertyName.objects.get(name=key)
#                     form = SongPropertyValueForm({'song': song_match.id, 'songpropertyname': value_match.id, 'value': value})
#                     if form.is_valid():
#                         form.save()
#                         out_list.append(f"Для песни: '{song_match}' свойству '{value_match}' присвоено значение '{value}'")
#                     else:
#                         out_list.append(f"{song_match.id} - {value_match.id} - {value}")
    
#     context.update({'out_list': out_list})
#     return render(request, 'chor/import.html', context)

# def importPerformances(request):
#     sl = SongList('chor/songlist.json').json_ready()
#     pl = PerformanceList()
#     pl.read_from_file('chor/performances.json')
#     out_list = list()
#     for item in pl.json_ready():
#         songo = Song.objects.get(name=sl[item['song_id']].get('name'))
#         dt = datetime.datetime(*map(int, item['date'].split('-')))
#         out_list.append(str(songo) + str(dt))
#         SongPerformance.objects.create(song=songo, datetime=dt)
#     context = {'out_list': out_list}
#     return render(request, 'chor/import.html', context)

def chorPerformances(request, chor_id):
    chor = Chor.objects.get(id=chor_id)
    # songs = Song.objects.filter(chor=chor).select_related('chor')
    performances = SongPerformance.objects.filter(song__chor=chor).order_by('-datetime')
    # perf = performances.filter(chor_id=chor_id)
    # for p in performances:
    #     print(p.__dir__())
    #     break
    context = {'chor': chor, 'performances': performances}
    return render(request, 'chor/chor-performances.html', context)