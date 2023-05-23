from .cmbot_songs import SongList
from .cmbot_performances import PerformanceList
from django.shortcuts import render, redirect
from .models import Song, SongPropertyValue, SongPropertyName, SongPerformance
from .forms import SongForm, SongPropertyNameForm, SongPropertyValueForm
import datetime

# Create your views here.

# songs = [
#     {'id': 1, 'name': 'Прихожу к тебе я'},
#     {'id': 2, 'name': 'Ты искупил мир от греха'},
#     {'id': 3, 'name': 'В Христе одном'},
# ]

def home(request):
    songs = Song.objects.filter(chor=1)
    context = {'songs': songs}
    return render(request, 'base/home.html', context)

def song(request, pk):
    song = Song.objects.get(id=pk)
    # attributes = []
    # for s in SongPropertyValue.objects.filter(song=pk):
    #     attributes.append(str(s))
    attributes = SongPropertyValue.objects.filter(song=pk)
    context = {'song': song, 'attributes': attributes}
    return render(request, 'base/song.html', context)

def createSong(request):
    form = SongForm()

    if request.method == "POST":
        form = SongForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/song_form.html', context)


def updateSong(request, pk):
    song = Song.objects.get(id = pk)
    form = SongForm(instance=song)

    if request.method == "POST":
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/song_form.html', context)

def deleteSong(request, pk):
    song = Song.objects.get(id=pk)
    if request.method == "POST":
        song.delete()
        return redirect('home')
    context = {'obj': song}
    return render(request, 'base/delete.html', context)

def importSonglist(request):
    sl = SongList('base/songlist.json').json_ready()
    
    out_list = list()
    context = dict()
    
    for songo in sl.values():
        if songo['status'] != 'deleted':
            song_match = Song.objects.get(name=songo['name'])
            for key, value in songo.items():
                if not key in ('status', 'name'):
                    value_match = SongPropertyName.objects.get(name=key)
                    form = SongPropertyValueForm({'song': song_match.id, 'songpropertyname': value_match.id, 'value': value})
                    if form.is_valid():
                        form.save()
                        out_list.append(f"Для песни: '{song_match}' свойству '{value_match}' присвоено значение '{value}'")
                    else:
                        out_list.append(f"{song_match.id} - {value_match.id} - {value}")
    
    context.update({'out_list': out_list})
    return render(request, 'base/import.html', context)

def importPerformances(request):
    sl = SongList('base/songlist.json').json_ready()
    pl = PerformanceList()
    pl.read_from_file('base/performances.json')
    out_list = list()
    for item in pl.json_ready():
        songo = Song.objects.get(name=sl[item['song_id']].get('name'))
        dt = datetime.datetime(*map(int, item['date'].split('-')))
        out_list.append(str(songo) + str(dt))
        SongPerformance.objects.create(song=songo, datetime=dt)
    context = {'out_list': out_list}
    return render(request, 'base/import.html', context)
