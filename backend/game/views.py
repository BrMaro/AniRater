from django.http import JsonResponse
from .utils import fetch_anime_by_difficulty
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Anime
import random

# Create your views here.


def random_anime(request, difficulty):
    anime_data = fetch_anime_by_difficulty(difficulty)

    if anime_data:
        return JsonResponse(anime_data)

    return JsonResponse({'error': 'Anime not found'}, status=404)

@api_view(['GET'])
def get_level_previews(request, level):
    """Get 3 anime previews for a specific difficulty level"""
    preview_count = 3
    previews = []
    
    for _ in range(preview_count):
        anime_data = fetch_anime_by_difficulty(level)
        if anime_data:
            # Only include necessary preview data
            preview = {
                'mal_id': anime_data['mal_id'],
                'title': anime_data['title'],
                'year': anime_data['year'],
                'images': anime_data['images'],
                'popularity': anime_data['popularity']
            }
            previews.append(preview)
    
    if previews:
        return Response(previews)
    
    return Response({'error': 'Failed to fetch previews'}, status=404)

# Optional: Async version for better performance
@api_view(['GET'])
async def get_level_previews_async(request, level):
    """Get 3 anime previews asynchronously for better performance"""
    preview_count = 3
    tasks = [fetch_anime_by_difficulty(level) for _ in range(preview_count)]
    
    try:
        previews = []
        for anime_data in tasks:
            if anime_data:
                preview = {
                    'mal_id': anime_data['mal_id'],
                    'title': anime_data['title'],
                    'year': anime_data['year'],
                    'images': anime_data['images'],
                    'popularity': anime_data['popularity']
                }
                previews.append(preview)
        
        if previews:
            return Response(previews)
            
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
    return Response({'error': 'Failed to fetch previews'}, status=404)