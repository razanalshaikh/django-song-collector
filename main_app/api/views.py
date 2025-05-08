from rest_framework.views import APIView
from main_app.models import Song, Artist, Album,Playlist
from .serializers import SongSerializer, AlbumSerializer,ArtistSerializer,PlaylistSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated, AllowAny

from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password 
from django.core.exceptions import ValidationError

class SingupView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        print(password)

        try:
            validate_password(password=password)
        except ValidationError as err:
            return Response({'error': err.messages} ,status=status.HTTP_400_BAD_REQUEST)
        
        # create user 
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        # create an access and refresh token 
        # for the user and send this in a response
        tokens = RefreshToken.for_user(user=user)
        return Response (
            { 'refresh':str(tokens), 'access': str(tokens.access_token)},
            status= status.HTTP_201_CREATED
        )

################# Function VIEW  ##################
# many to many relationship with Playlist model and song model
# add song
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_song_to_playlist(request,playlist_id,song_id):
    try:
        # GET the playlist by playlist_id 
        playlist = Playlist.objects.get(pk=playlist_id)
        #print(playlist)
        # Get the song by song_id
        song = Song.objects.get(pk=song_id)
        #print(song)
        # add the song to the playlist
        if playlist.songs.filter(id=song_id).exists():
            return Response({'message': 'The the song already exists in the playlist!'})
        else:    
            playlist.songs.add(song)
            return Response({'message':'song was Added!'},status=201)
    except Playlist.DoesNotExist:
        return Response({'error':'the playlist does not exists'},status=404)
    except Song.DoesNotExist:
        return Response({'error':'the song does not exists'},status=404)
    except:
        return Response({'error':'Something went Wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# remove song
@api_view(['POST'])
def remove_song_from_playlist(request,playlist_id,song_id):
    try:
        # GET the playlist by playlist_id 
        playlist = Playlist.objects.get(pk=playlist_id)
        print(playlist)
        # Get the song by song_id
        song = Song.objects.get(pk=song_id)
        print(song)
        # remove the song to the playlist if exists
        if playlist.songs.filter(id=song_id).exists():
            playlist.songs.remove(song)
            return Response({'message':'song removed!'},status=status.HTTP_200_OK)
        else: 
            # not exist show message
            return Response({'message': 'The song is in the DB but it is not on the playlist!'})    
    except Playlist.DoesNotExist:
        return Response({'error':'the playlist does not exists'},status=404)
    except Song.DoesNotExist:
        return Response({'error':'the song does not exists'},status=404)
    except:
        return Response({'error':'Something went Wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

################## CLASS-BASED VIEW  ##################
class SongListAPI(APIView):

    def get(self,request):
        # get all songs from the DB
        songs = Song.objects.all()
        # serializer our songs into JSON
        serializer = SongSerializer(songs,many=True)
        return Response(serializer.data)

    def post(self, request):
        # De-serialize our data
        serializer = SongSerializer(data=request.data)
        # if valid return response of 201 created
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        # if anything happens, erorr then 400 bad request
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    # I created this so I can see all the artists 
class ArtistListAPI(APIView):
    def get(self,request):
        # get all songs from the DB
        artists = Artist.objects.all()
        # serializer our songs into JSON
        serializer = ArtistSerializer(artists,many=True)
        return Response(serializer.data)

    def post(self, request):
        # De-serialize our data
        serializer = ArtistSerializer(data=request.data)
        # if valid return response of 201 created
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        # if anything happens, erorr then 400 bad request
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class AlbumAPI(APIView):
    def get(self, request, artist_id):
        artist = get_object_or_404(Artist,pk=artist_id)
        albums = Album.objects.filter(artist_id = artist.pk)
        serializer = AlbumSerializer(albums,many=True)
        return Response(serializer.data)

    def post(self,request,artist_id):
        #  the artist id will be passed into get_object_or_404 function, 
        # it will return the artist obj if exists, or it will raise a 404
        # if it doesnt exist 
        artist = get_object_or_404(Artist,pk=artist_id)
        data = request.data.copy() # make a copy
        data['artist'] = artist.id # add the artist to the ablum
        
        serializer = AlbumSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=400)

class PlaylistListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        # get all songs from the DB
        playlist = Playlist.objects.filter(user=request.user)
        # serializer our songs into JSON
        serializer = PlaylistSerializer(playlist,many=True)
        return Response(serializer.data)

    def post(self, request):
        # De-serialize our data
        serializer = PlaylistSerializer(data=request.data)
        # if valid return response of 201 created
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        # if anything happens, erorr then 400 bad request
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    