from django.forms import ModelForm
from .models import Song, SongPropertyName, SongPropertyValue

class SongForm(ModelForm):
    class Meta:
        model = Song
        fields = '__all__'

class SongPropertyNameForm(ModelForm):
    class Meta:
        model = SongPropertyName
        fields = '__all__'

class SongPropertyValueForm(ModelForm):
    class Meta:
        model = SongPropertyValue
        fields = '__all__'

        