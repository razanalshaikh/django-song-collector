from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import Song, Artist, Album, Playlist
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView
from .forms import AlbumForm

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.
# signup
def signup(request):
    # prevent user from seeing signup form
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('home')
        
    form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# home page
def home(request):
    return render(request, 'home.html')

class SongListView(LoginRequiredMixin,ListView):
    model = Song
    template_name = 'song_list.html'
    context_object_name = 'songs'

class SongDetailView(LoginRequiredMixin,DetailView):
    model = Song
    template_name = 'song_detail.html'
    context_object_name = 'song'

# make sure that the user should be an is_superuser in specific views
# I searched about it :https://stackoverflow.com/questions/51284583/authentication-for-class-based-views-in-django
# I will use AdminStaffRequiredMixin to check if it's admin logged-in
class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

class CreateSongView(AdminStaffRequiredMixin,CreateView):
    model = Song
    fields = ['title', 'artist', 'date', 'link']
    template_name = 'song_form.html'
    success_url = reverse_lazy('song_list')

class UpdateSongView(AdminStaffRequiredMixin,UpdateView):
    model = Song
    fields = ['title', 'artist', 'date', 'link']
    template_name = 'song_form.html'
    success_url = reverse_lazy('song_list')

class DeleteSongView(AdminStaffRequiredMixin,DeleteView):
    model = Song
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('song_list')

    # Artist model 
class ArtistListView(LoginRequiredMixin, ListView):
    model = Artist
    template_name = 'artist_list.html'
    context_object_name = 'artists'

@login_required
def artist_detail_view(request,artist_id):
    artist = Artist.objects.get(id = artist_id)
    album_form = AlbumForm()

    return render(request,'artist_detail.html',{ 
        'artist': artist, 
        'album_form': album_form
    })
@login_required
def add_album_to_artist(request,artist_id):
    form = AlbumForm(request.POST)
    if form.is_valid():
        new_song = form.save(commit=False)
        # add song id to db
        new_song.artist_id = artist_id
        new_song.save()# save to DB
    # redirect the uset to same page
    return redirect('artist_detail',artist_id = artist_id)

class CreateArtistView(AdminStaffRequiredMixin,CreateView):
    model = Artist
    fields = ['name']
    template_name = 'artist_form.html'
    success_url = reverse_lazy('artist_list')    

class UpdateArtistView(AdminStaffRequiredMixin,UpdateView):
    model = Artist
    fields = ['name']
    template_name = 'artist_form.html'
    success_url = reverse_lazy('artist_list')

class DeleteArtistView(AdminStaffRequiredMixin,DeleteView):
    model = Artist
    template_name = 'confirm_delete_artist.html'
    success_url = reverse_lazy('artist_list')


#############    playlist     #############
# adding a playlist, each user will have many playlist 
## each user can create a playlist and add songs to it
## I will use LoginRequiredMixin which is for class based view
class PlayListView(LoginRequiredMixin,ListView):
    model = Playlist
    template_name = 'playlist_list.html'
    context_object_name = 'playlist' 
    def get_queryset(self):
        return Playlist.objects.filter(user = self.request.user)

class CreatePlaylist(LoginRequiredMixin,CreateView):
    model = Playlist
    fields = ['name']
    template_name = 'playlist_form.html'
    success_url = reverse_lazy('playlist_list')    
    
    def form_valid(self, form):
        # Assign the logged in user  to the form instance
        form.instance.user = self.request.user 
        return super().form_valid(form)
    
class UpdatePlaylist(LoginRequiredMixin,UpdateView):
    model = Playlist
    fields = ['name']
    template_name = 'playlist_form.html'
    success_url = reverse_lazy('playlist_list') 

class DeletePlaylistView(LoginRequiredMixin,DeleteView):
    model = Playlist
    template_name = 'confirm_delete_playlist.html'
    success_url = reverse_lazy('playlist_list') 

@login_required
def playlist_detail_view(request,playlist_id):
    playlist = Playlist.objects.get(id=playlist_id)
    songs_playlist_does_not_have = Song.objects.exclude(id__in = playlist.songs.all().values_list('id'))
    return render (request, 'playlist_detail.html',{
        'playlist': playlist,
        'songs_playlist_does_not_have': songs_playlist_does_not_have
    })

@login_required
def assoc_song(request,playlist_id,song_id):
    # add a song to playlist
    Playlist.objects.get(id = playlist_id).songs.add(song_id)
    return redirect('playlist_detail',playlist_id = playlist_id)
@login_required
def dessoc_song(request,playlist_id,song_id):
    # delete a specific song from playlist
    Playlist.objects.get(id=playlist_id).songs.remove(song_id)
    return redirect('playlist_detail',playlist_id = playlist_id)
