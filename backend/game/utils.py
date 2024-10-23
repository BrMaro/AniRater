# your_app/utils.py
import pprint
import random
import requests
import aiohttp
import time
from django.conf import settings
from.models import Anime
import asyncio
# from .models import Anime

JIKAN_API_URL = 'https://api.jikan.moe/v4'


def fetch_anime_from_jikan(mal_id):
    url = f'{JIKAN_API_URL}/anime/{mal_id}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['data']  # Return the 'data' section from the response
    else:
        print(f"Error fetching anime data: {response.status_code}")
        return None


# print(fetch_anime_from_jikan(1))


def fetch_anime_by_difficulty(level):
    if level == 1:  # Very Easy
        start, end = 1, 250
    elif level == 2:  # Easy
        start, end = 251, 500
    elif level == 3:  # Medium
        start, end = 501, 1000
    elif level == 4:  # Hard
        start, end = 1001, 3000
    elif level == 5:  # Very Hard
        start, end = 3001, 5000
    elif level == 6:  # God Mode
        start, end = 5001, 999999  # No upper limit

    # Calculate the number of pages needed
    page_start = start // 50 + 1
    page_end = end // 50

    random_page = random.randint(page_start, page_end)

    url = f'{JIKAN_API_URL}/top/anime?filter=bypopularity&limit=25&page={random_page}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        anime_list = data['data']

        if anime_list:
            selected_anime = random.choice(anime_list)

            anime_details_url = f"{JIKAN_API_URL}/anime/{selected_anime['mal_id']}"
            details_response = requests.get(anime_details_url)

            if details_response.status_code == 200:
                details_data = details_response.json()

                anime_details = details_data['data']

                return {
                    'mal_id': selected_anime['mal_id'],
                    'title': selected_anime['title'],
                    'type': selected_anime['type'],
                    'year': selected_anime['aired']['prop']['from']['year'],
                    'url': f'https://myanimelist.net/anime/{selected_anime["mal_id"]}/{selected_anime["title"].replace(" ", "_")}',
                    'images': {
                        'image_url': selected_anime['images']['jpg']['image_url'],
                        'large_image_url': selected_anime['images']['jpg']['large_image_url'],
                    },
                    'episodes': selected_anime.get('episodes', 'N/A'),
                    'favorites': selected_anime.get('favorites', 0),
                    'genres': [genre['name'] for genre in selected_anime['genres']],
                    'members': selected_anime['members'],
                    'popularity': selected_anime['popularity'],
                    'rank': selected_anime['rank'],
                    'score': selected_anime['score'],
                    'scored_by': selected_anime['scored_by'],
                    'synopsis': selected_anime['synopsis'],
                    'youtube_url': selected_anime.get('trailer', {}).get('url', 'N/A'),
                }

    else:
        print(f"Error fetching anime data: {response.status_code}, {response.text}")

    return None


# pprint.pprint(fetch_anime_by_difficulty(1)) 
async def fetch_anime_from_jikan_async(session, mal_id):
    url = f'{JIKAN_API_URL}/anime/{mal_id}'
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            return data['data']
        else:
            print(f"Error fetching anime data: {response.status}")
            return None
        
        
async def fetch_anime_by_difficulty_async(level):
    if level == 1:  # Very Easy
        start, end = 1, 250
    elif level == 2:  # Easy
        start, end = 251, 500
    elif level == 3:  # Medium
        start, end = 501, 1000
    elif level == 4:  # Hard
        start, end = 1001, 3000
    elif level == 5:  # Very Hard
        start, end = 3001, 5000
    elif level == 6:  # God Mode
        start, end = 5001, 999999  # No upper limit

    # Calculate the number of pages needed
    page_start = start // 50 + 1
    page_end = end // 50

    random_page = random.randint(page_start, page_end)

    url = f'{JIKAN_API_URL}/top/anime?filter=bypopularity&limit=25&page={random_page}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                anime_list = data['data']

                if anime_list:
                    selected_anime = random.choice(anime_list)
                    anime_details = await fetch_anime_from_jikan_async(session, selected_anime['mal_id'])

                    if anime_details:
                        return {
                            'mal_id': selected_anime['mal_id'],
                            'title': selected_anime['title'],
                            'type': selected_anime['type'],
                            'year': selected_anime['aired']['prop']['from']['year'],
                            'url': f'https://myanimelist.net/anime/{selected_anime["mal_id"]}/{selected_anime["title"].replace(" ", "_")}',
                            'images': {
                                'image_url': selected_anime['images']['jpg']['image_url'],
                                'large_image_url': selected_anime['images']['jpg']['large_image_url'],
                            },
                            'episodes': selected_anime.get('episodes', 'N/A'),
                            'favorites': selected_anime.get('favorites', 0),
                            'genres': [genre['name'] for genre in selected_anime['genres']],
                            'members': selected_anime['members'],
                            'popularity': selected_anime['popularity'],
                            'rank': selected_anime['rank'],
                            'score': selected_anime['score'],
                            'scored_by': selected_anime['scored_by'],
                            'synopsis': selected_anime['synopsis'],
                            'youtube_url': selected_anime.get('trailer', {}).get('url', 'N/A'),
                        }

            else:
                print(f"Error fetching anime data: {response.status}")

    return None


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