# your_app/utils.py
import pprint
import random
import requests
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
    # Define the ranges based on difficulty level
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
    page_start = start // 50 + 1  # Jikan API has a maximum of 25 items per page
    page_end = end // 50   # Calculate the last page number to fetch
    print(page_start, page_end)
    # Randomly select a page within the range of pages to fetch
    random_page = random.randint(page_start, page_end)

    # Fetch the anime data from the randomly selected page
    url = f'{JIKAN_API_URL}/top/anime?filter=bypopularity&limit=25&page={random_page}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        anime_list = data['data']

        if anime_list:
            # Randomly select one anime from the list
            selected_anime = random.choice(anime_list)
            # Fetch additional details for the selected anime
            anime_details_url = f"{JIKAN_API_URL}/anime/{selected_anime['mal_id']}"
            details_response = requests.get(anime_details_url)

            if details_response.status_code == 200:
                details_data = details_response.json()

                anime_details = details_data['data']

                return {
                    'mal_id': anime_details['mal_id'],
                    'url': anime_details['url'],
                    'images': anime_details['images'],
                    'trailer': anime_details.get('trailer', None),
                    'approved': anime_details.get('approved', None),
                    'titles': anime_details.get('titles', []),
                    'title': anime_details['title'],
                    'title_english': anime_details.get('title_english', None),
                    'title_japanese': anime_details.get('title_japanese', None),
                    'title_synonyms': anime_details.get('title_synonyms', []),
                    'type': anime_details.get('type', None),
                    'source': anime_details.get('source', None),
                    'episodes': anime_details.get('episodes', None),
                    'status': anime_details.get('status', None),
                    'airing': anime_details.get('airing', None),
                    'aired': anime_details.get('aired', None),
                    'duration': anime_details.get('duration', None),
                    'rating': anime_details.get('rating', None),
                    'score': anime_details.get('score', None),
                    'scored_by': anime_details.get('scored_by', None),
                    'rank': anime_details.get('rank', None),
                    'popularity': anime_details.get('popularity', None),
                    'members': anime_details.get('members', None),
                    'favorites': anime_details.get('favorites', None),
                    'synopsis': anime_details.get('synopsis', None),
                    'background': anime_details.get('background', None),
                    'season': anime_details.get('season', None),
                    'year': anime_details.get('year', None),
                    'producers': anime_details.get('producers', []),
                    'studios': anime_details.get('studios', []),
                    'genres': anime_details.get('genres', []),
                    'explicit_genres': anime_details.get('explicit_genres', []),
                    'themes': anime_details.get('themes', []),
                    'demographics': anime_details.get('demographics', []),
                }

    else:
        print(f"Error fetching anime data: {response.status_code}, {response.text}")

pprint.pprint(fetch_anime_by_difficulty(1))