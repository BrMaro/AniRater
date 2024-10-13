from django.http import JsonResponse
from .utils import fetch_anime_by_difficulty

# Create your views here.


def random_anime(request, difficulty):
    anime_data = fetch_anime_by_difficulty(difficulty)

    if anime_data:
        return JsonResponse(anime_data)

    return JsonResponse({'error': 'Anime not found'}, status=404)