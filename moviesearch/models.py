from django.conf import settings
from django.db import models

class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie_id = models.IntegerField()  # Assuming you are storing movie_id as an integer

    def __str__(self):
        return f'{self.user.username} - {self.movie_id}'

class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    overview = models.TextField()
    release_date = models.CharField(max_length=10)
    poster_path = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title
