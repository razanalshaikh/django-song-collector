from rest_framework import serializers
from main_app.models import Song, Album, Artist, Playlist

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__' # this will bring all fields 

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

class  PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'


