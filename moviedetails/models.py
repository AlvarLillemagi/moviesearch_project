from django.conf import settings
from django.db import models

class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie_id = models.IntegerField()

    def __str__(self):
        return f'{self.user.username} - {self.movie_id}'