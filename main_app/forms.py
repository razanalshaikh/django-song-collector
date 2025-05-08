from django.forms import ModelForm
from .models import Album

class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ['album_title','language']