from django.urls import path
from .views import (
    SongListView,
    SongDetailView, 
    CreateSongView, 
    UpdateSongView, 
    DeleteSongView,
    ArtistListView,
    CreateArtistView,
    DeleteArtistView,
    UpdateArtistView,
    artist_detail_view,
    add_album_to_artist,
    PlayListView,
    CreatePlaylist,
    UpdatePlaylist,
    DeletePlaylistView,
    playlist_detail_view,
    assoc_song,
    dessoc_song,
    home,
    signup
)

urlpatterns = [
    path('', home, name='home'),
    path('accounts/signup',signup,name='signup'),

    path('all-songs/', SongListView.as_view(),name="song_list"),
    path('all-songs/<int:pk>',SongDetailView.as_view(),name='song_detail'),
    path('all-songs/add',CreateSongView.as_view(), name='song_create'),
    path('all-songs/<int:pk>/update',UpdateSongView.as_view(),name='song_update'),
    path('all-songs/<int:pk>/delete',DeleteSongView.as_view(), name="song_delete"),
    
    path('all-artists/',ArtistListView.as_view(),name='artist_list'),
    path('all-artists/add',CreateArtistView.as_view(),name='artist_create'),
    path('all-artists/<int:artist_id>/',artist_detail_view,name='artist_detail'),
    path('all-artists/<int:pk>/update',UpdateArtistView.as_view(),name='artist_update'),
    path('all-artists/<int:pk>/delete',DeleteArtistView.as_view(), name="artist_delete"),
    path('all-artists/<int:artist_id>/add-song',add_album_to_artist,name='add_album_to_artist'),    
    
    path('all-playlists/', PlayListView.as_view(),name='playlist_list'),
    path('all-playlists/add', CreatePlaylist.as_view(),name='playlist_create'),
    path('all-playlists/<int:pk>/update',UpdatePlaylist.as_view(),name='playlist_update'),
    path('all-playlists/<int:pk>/delete',DeletePlaylistView.as_view(),name='playlist_delete'),
    path('all-playlists/<int:playlist_id>/',playlist_detail_view,name='playlist_detail'),
    path('all-playlists/<int:playlist_id>/assoc-song/<int:song_id>',assoc_song,name='assoc_song'),
    path('all-playlists/<int:playlist_id>/dessoc-song/<int:song_id>',dessoc_song,name='dessoc_song')

    ]
