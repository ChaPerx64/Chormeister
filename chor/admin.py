from django.contrib import admin

# Register your models here.

from .models import Song, Chor, SongPropertyName, SongPropertyValue, SongPerformance

admin.site.register(Song)
admin.site.register(Chor)
admin.site.register(SongPropertyName)
admin.site.register(SongPropertyValue)
admin.site.register(SongPerformance)