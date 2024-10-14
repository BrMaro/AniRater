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