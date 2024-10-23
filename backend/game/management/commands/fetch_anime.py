from django.core.management.base import BaseCommand
import time
import requests
from game.models import Anime

class Command(BaseCommand):
    help = 'Fetches anime data from Jikan API and stores it in the database'

    def handle(self, *args, **options):
        base_url = "https://api.jikan.moe/v4/anime"
        
        for mal_id in range(1, 30001):
            try:
                if Anime.objects.filter(mal_id=mal_id).exists():
                    self.stdout.write(f"Anime {mal_id} already exists in DB. Skipping...")
                    continue
                    
                if mal_id > 1 and mal_id % 3 == 0:
                    time.sleep(1)
                
                response = requests.get(f"{base_url}/{mal_id}")
                response.raise_for_status()
                data = response.json()['data']
                
                genres = ','.join([genre['name'] for genre in data.get('genres', [])])
                
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
                self.stdout.write(self.style.SUCCESS(f"Successfully stored anime {mal_id}"))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error fetching/storing anime {mal_id}: {str(e)}"))
                continue