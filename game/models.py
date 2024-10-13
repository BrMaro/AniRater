from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Anime(models.Model):
    mal_id = models.IntegerField(unique=True)  # ID from MyAnimeList
    title = models.CharField(max_length=255)
    poster_url = models.URLField()
    release_date = models.DateField()
    genres = models.CharField(max_length=255)
    synopsis = models.TextField()
    youtube_summary_url = models.URLField()
    rating = models.FloatField()  # MAL rating

    def __str__(self):
        return self.title
    
class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    score = models.IntegerField(default=100)  # Start with 100, deduct with clues unlocked
    clues_unlocked = models.IntegerField(default=0)
    guess = models.FloatField(null=True, blank=True)  # User guess for the rating
    created_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    badges = models.ManyToManyField('Badge', blank=True)
    streak = models.IntegerField(default=0)

class Badge(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followed', on_delete=models.CASCADE)