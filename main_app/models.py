from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=100)
    link = models.URLField()
    date = models.DateField()

    def __str__(self):
        return f"{self.artist} - {self.title}"
    

class Artist(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

LANGUAGE = (
    ('en', 'English'),
    ('ar', 'Arabic'),
    ('tr', 'Turkish'),
    ('fr', 'French'),
    ('es', 'Spanish'),
    ('de', 'German'),
    ('zh', 'Chinese'),
    ('jp', 'Japanese')
)

class Album(models.Model):
    album_title = models.CharField()
    language = models.CharField(
        max_length= 2,
        choices= LANGUAGE,
        default=LANGUAGE[0][0]
    )
    artist = models.ForeignKey(Artist,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.album_title} - {self.get_language_display()}"

class Playlist(models.Model):
    name = models.CharField(max_length=50)
    songs = models.ManyToManyField(Song)
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
