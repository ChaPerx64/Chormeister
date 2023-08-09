import json
import subprocess
from django.shortcuts import render
from django.http import FileResponse, HttpResponse, HttpResponseForbidden
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.handlers.wsgi import WSGIRequest
from chor.models import Song, SongPropertyName, SongPropertyValue, SongPerformance
from cmdjango.settings import BASE_DIR


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


@api_view(['GET'])
def getJsonDump(request: WSGIRequest):
    if request.user.is_superuser:
        output = subprocess.run(['sh', BASE_DIR / 'bash' / 'dumpdata.sh'], capture_output=True)
        out_dict = json.loads(output.stdout)
        if output.returncode == 0:
            return Response(out_dict)
        return Response({'status': str(output.stderr)})
    return HttpResponseForbidden('ACCESS DENIED')


# @api_view(['POST'])
def loadFromJson(request: WSGIRequest):
    if request.user.is_superuser:
        if request.method == "POST":
            if request.FILES.get('jsonfile'):
                sjson = request.FILES['jsonfile']
                with open(BASE_DIR / "dumps" / "dump.json", "wb+") as destination:
                    for chunk in sjson.chunks():
                        destination.write(chunk)
                # print('READING WITH PYTHON...')
                # with open(BASE_DIR / "dumps" / "dump.json", "r") as f:
                #     print(f.read())
                print("LOADING WITH DJANGO...")
                output = subprocess.run(['sh', BASE_DIR / 'bash' / 'reloadfromdump.sh'], capture_output=True)
                return HttpResponse(
                    f'''<h1>LOAD RESULTS</h1><h2>STDOUT</h2>
                    <pre>{str(output.stdout.decode())}</pre>
                    <h2>STDERR</h2>
                    <pre>{str(output.stderr.decode())}</pre>
                    '''
                )
            else:
                print('no file')
        context = {
            
        }
        return render(request, 'reload-base.html', context)
    return HttpResponseForbidden('ACCESS DENIED')
