from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Anime:
    def __init__(self, mal_id, title, anime_type, year, url, image_url,
                 large_image_url, episodes, favorites, genres, members,
                 popularity, rank, score, scored_by, synopsis, youtube_url):
        self.mal_id = mal_id
        self.title = title
        self.type = anime_type
        self.year = year
        self.url = url
        self.image_url = image_url
        self.large_image_url = large_image_url
        self.episodes = episodes
        self.favorites = favorites
        self.genres = genres
        self.members = members
        self.popularity = popularity
        self.rank = rank
        self.score = score
        self.scored_by = scored_by
        self.synopsis = synopsis
        self.youtube_url = youtube_url

    def __str__(self):
    
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