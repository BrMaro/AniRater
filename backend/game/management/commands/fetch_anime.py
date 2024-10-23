from django.core.management.base import BaseCommand
from django.core.cache import cache
import time
import requests
from game.models import Anime
import json
import os

class Command(BaseCommand):
    help = 'Fetches anime data from Jikan API and stores it in the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset the progress and start from beginning',
        )

    def get_progress(self):
        """Get the last processed MAL ID from cache or progress file"""
        # Try to get from cache first
        last_id = cache.get('anime_fetch_progress')
        
        if last_id is None:
            # If not in cache, try to get from file
            try:
                with open('anime_fetch_progress.json', 'r') as f:
                    data = json.load(f)
                    last_id = data.get('last_mal_id', 0)
            except (FileNotFoundError, json.JSONDecodeError):
                last_id = 0
                
        return last_id

    def save_progress(self, mal_id):
        """Save the current progress to both cache and file"""
        # Save to cache
        cache.set('anime_fetch_progress', mal_id, timeout=None)
        
        # Save to file as backup
        with open('anime_fetch_progress.json', 'w') as f:
            json.dump({'last_mal_id': mal_id}, f)
            
    def handle(self, *args, **options):
        base_url = "https://api.jikan.moe/v4/anime"
        
        # Reset progress if requested
        if options['reset']:
            self.save_progress(0)
            self.stdout.write(self.style.WARNING("Progress reset to beginning"))
        
        # Get the last processed ID
        start_id = self.get_progress() + 1
        self.stdout.write(f"Starting from MAL ID: {start_id}")
        
        for mal_id in range(start_id, 30001):
            try:
                # Save progress at the start of each iteration
                self.save_progress(mal_id - 1)
                
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
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    self.stdout.write(f"Anime {mal_id} not found. Skipping...")
                    continue
                self.stdout.write(self.style.ERROR(f"HTTP Error for anime {mal_id}: {str(e)}"))
                # Wait longer for HTTP errors
                time.sleep(5)
                continue
                
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f"Network error for anime {mal_id}: {str(e)}"))
                # Wait even longer for network errors
                time.sleep(10)
                continue
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error fetching/storing anime {mal_id}: {str(e)}"))
                continue
        
        # Save final progress
        self.save_progress(30000)
        self.stdout.write(self.style.SUCCESS("Finished fetching all anime"))