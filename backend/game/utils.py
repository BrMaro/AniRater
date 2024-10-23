import random
from .models import Anime



def fetch_anime_by_difficulty(level):
    """Fetch anime by difficulty level from the database"""
    if level == 1:  # Very Easy
        popularity_range = (1, 250)
    elif level == 2:  # Easy
        popularity_range = (251, 500)
    elif level == 3:  # Medium
        popularity_range = (501, 1000)
    elif level == 4:  # Hard
        popularity_range = (1001, 3000)
    elif level == 5:  # Very Hard
        popularity_range = (3001, 5000)
    else:  # God Mode
        popularity_range = (5001, 999999)
    
    anime_queryset = Anime.objects.filter(
        popularity__gte=popularity_range[0],
        popularity__lte=popularity_range[1]
    )
    
    if anime_queryset.exists():
        anime = random.choice(anime_queryset)
        return anime_to_dict(anime)
    
    return None


def anime_to_dict(anime):
    """Convert Anime model instance to dictionary format matching the original API response"""
    return {
        'mal_id': anime.mal_id,
        'title': anime.title,
        'year': anime.year,
        'url': anime.url,
        'images': {
            'image_url': anime.image_url,
            'large_image_url': anime.large_image_url,
        },
        'episodes': anime.episodes,
        'favorites': anime.favorites,
        'genres': anime.genres_list,
        'members': anime.members,
        'popularity': anime.popularity,
        'rank': anime.rank,
        'score': anime.score,
        'scored_by': anime.scored_by,
        'synopsis': anime.synopsis,
        'youtube_url': anime.youtube_url,
    }

