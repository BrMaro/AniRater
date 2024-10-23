from django.db import models
from users.models import User
from django.utils import timezone

# Create your models here.

# models.py
from django.db import models

class Anime(models.Model):
    mal_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    anime_type = models.CharField(max_length=50)
    year = models.IntegerField(null=True)
    url = models.URLField()
    image_url = models.URLField()
    large_image_url = models.URLField()
    episodes = models.IntegerField(null=True)
    favorites = models.IntegerField(default=0)
    members = models.IntegerField(default=0)
    popularity = models.IntegerField(null=True)
    rank = models.IntegerField(null=True)
    score = models.FloatField(null=True)
    scored_by = models.IntegerField(default=0)
    synopsis = models.TextField(null=True, blank=True)
    youtube_url = models.URLField(null=True, blank=True)
    
    # Store genres as comma-separated string
    genres = models.TextField()
    
    # Add timestamps for tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['mal_id']),
            models.Index(fields=['title']),
        ]
    
    def __str__(self):
        return self.title
    
    @property
    def genres_list(self):
        """Convert stored genres string to list"""
        return [genre.strip() for genre in self.genres.split(',') if genre.strip()]


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
