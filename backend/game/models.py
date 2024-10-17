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
        return self.title


class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=100)  # Deduct score as clues are unlocked
    guess = models.FloatField(null=True, blank=True)  # User guess for the anime rating
    created_at = models.DateTimeField(auto_now_add=True)
    # start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)

    # def set_end_time(self):
    #     self.end_time = timezone.now()

    # def get_total_time(self):
    #     if self.end_time:
    #         return self.end_time - self.start_time
    #     return None


