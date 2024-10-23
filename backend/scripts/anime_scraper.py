import time
import requests
import os
import django
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)
print(project_root)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AniRater.settings')  # Adjust this to your project name
django.setup()

# Now import your model
from game.models import Anime  # Adjust 'game' to your app name



def fetch_and_store_anime(anime_ids):
    """
    Fetch anime data from Jikan API and store in database
    
    Args:
        anime_ids (list): List of MAL IDs to fetch
    """
    base_url = "https://api.jikan.moe/v4/anime"
    
    for i, mal_id in enumerate(anime_ids):
        try:
            # Check if anime already exists in DB
            if Anime.objects.filter(mal_id=mal_id).exists():
                print(f"Anime {mal_id} already exists in DB. Skipping...")
                continue
                
            # Respect rate limit (3 requests per second)
            if i > 0 and i % 3 == 0:
                time.sleep(1)
            
            # Fetch from Jikan
            response = requests.get(f"{base_url}/{mal_id}")
            response.raise_for_status()
            data = response.json()['data']
            
            # Extract genres
            genres = ','.join([genre['name'] for genre in data.get('genres', [])])
            
            # Create AnimeModel instance
            anime = Anime(
                mal_id=data['mal_id'],
                title=data['title'],
                anime_type=data['type'],
                year=data.get('year'),
                url=data['url'],
                image_url=data['images']['jpg']['image_url'],
                large_image_url=data['images']['jpg']['large_image_url'],
                episodes=data.get('episodes'),
                favorites=data.get('favorites', 0),
                genres=genres,
                members=data.get('members', 0),
                popularity=data.get('popularity'),
                rank=data.get('rank'),
                score=data.get('score'),
                scored_by=data.get('scored_by', 0),
                synopsis=data.get('synopsis'),
                youtube_url=data.get('trailer', {}).get('url')
            )
            anime.save()
            print(f"Successfully stored anime {mal_id}")
            
        except Exception as e:
            print(f"Error fetching/storing anime {mal_id}: {str(e)}")
            continue

mal_ids = [i for i in range(30000)]
fetch_and_store_anime(mal_ids)