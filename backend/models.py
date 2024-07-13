from django.db import models

# Create your models here.
from django.db import models

class Song(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.TextField()
    artist = models.TextField()
    danceability = models.FloatField()
    energy = models.FloatField()
    key = models.IntegerField()
    loudness = models.FloatField()
    mode = models.IntegerField()
    speechiness = models.FloatField()
    acousticness = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    valence = models.FloatField()
    tempo = models.FloatField()

    def __str__(self):
        return f"{self.name} by {self.artist}"