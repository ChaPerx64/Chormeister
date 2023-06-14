from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.handlers.wsgi import WSGIRequest
from chor.models import Song, SongPropertyName, SongPropertyValue, SongPerformance


@api_view(['GET'])
def getChorSongsJson(request: WSGIRequest):
    chor_id = request.GET.get('c')
    songs = Song.objects.filter(chor__id=chor_id)
    songpropnames = SongPropertyName.objects.filter(chor__id=chor_id)
    out_dict = dict()
    for song in songs:
        song_dict = {'name': song.name}
        for propname in songpropnames:
            try:
                value = SongPropertyValue.objects.get(song=song, songpropertyname=propname).value
            except:
                value = ''
            song_dict.update({propname.name: value})
        out_dict.update({str(song.pk): song_dict})
    return Response(out_dict)


@api_view(['GET'])
def getChorPerformancesJson(request: WSGIRequest):
    chor_id = request.GET.get('c')
    perfs = SongPerformance.objects.filter(song__chor__id=chor_id)
    out_list = list()
    for perf in perfs:
        out_list.append(
            {
                'song_id': str(perf.song.pk),
                'date': perf.dtofperformance.isoformat().split('T')[0],
            }
        )
    return Response(out_list)

