from django.urls import path 
from .views import (
    SongListAPI, 
    AlbumAPI,
    ArtistListAPI, 
    add_song_to_playlist, 
    remove_song_from_playlist, 
    PlaylistListAPI,
    SingupView)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('songs/', SongListAPI.as_view(),name='api_songs'),
    
    path('artists/',ArtistListAPI.as_view(),name = 'api_artists'),
    path('artists/<int:artist_id>/albums', AlbumAPI.as_view(),name='api_albums'),
    
    path('playlists/<int:playlist_id>/add-songs/<int:song_id>',add_song_to_playlist,name='api_add_song_to_playlist'),
    path('playlists/<int:playlist_id>/remove-songs/<int:song_id>',remove_song_from_playlist,name='api_remove_song_from_playlist'),
    path('playlists/',PlaylistListAPI.as_view(),name='api_playlist'),
    path('token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/',SingupView.as_view(), name='signup')
]