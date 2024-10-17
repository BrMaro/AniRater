from django.db import models
from users.models import User
from django.utils import timezone

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
    score = models.IntegerField(default=0)  
    games_played = models.IntegerField(default=0)  
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)

    def start_session(self):
        """Start a new game session."""
        self.start_time = timezone.now()
        self.save()

    def end_session(self):
        """End the game session and save the end time."""
        self.end_time = timezone.now()
        self.save()

    def add_game(self, game_score):
        """Add a new game to the session and accumulate the score."""
        self.score += game_score  # Add the game's score to the total score
        self.games_played += 1  # Increment the number of games played
        self.save()

    def get_total_time(self):
        """Calculate the total duration of the game session."""
        if self.end_time:
            return self.end_time - self.start_time
        return None

    def __str__(self):
        return f'GameSession(user={self.user.username}, score={self.score}, games_played={self.games_played})'
