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
    page_start = start // 25 + 1  # Jikan API has a maximum of 25 items per page
    pages_needed = (end - start) // 25 + 1  # Calculate how many pages we need

    all_anime = []

    for page in range(page_start, page_start + pages_needed):
        url = f'{JIKAN_API_URL}/top/anime?type=tv&limit=25&page={page}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            anime_list = data['data']
            all_anime.extend(anime_list)
        else:
            print(f"Error fetching anime data: {response.status_code}, {response.text}")
            return None

    if all_anime:
        # Randomly select one anime from the collected list
        selected_anime = random.choice(all_anime)
        return {
            'mal_id': selected_anime['mal_id'],
            'title': selected_anime['title'],
            'poster_url': selected_anime['images']['jpg']['large_image_url'],
            'release_date': selected_anime['aired']['string'],
            'genres': ', '.join([genre['name'] for genre in selected_anime['genres']]),
            'synopsis': selected_anime['synopsis'],
        }

    return None


print(fetch_anime_by_difficulty(1))