from django.http import JsonResponse
from .utils import fetch_anime_by_difficulty
from .utils import fetch_anime_by_difficulty_async
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
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
    try:
        preview_count = 3
        # Create tasks for fetching previews
        tasks = [fetch_anime_by_difficulty_async(level) for _ in range(preview_count)]
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks)
        
        # Filter out None results and format the previews
        previews = []
        for anime_data in results:
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
        
        return Response(
            {'error': 'Failed to fetch previews'}, 
            status=404
        )
            
    except Exception as e:
        print(f"Error in get_level_previews: {str(e)}")  # Add logging
        return Response(
            {'error': f'Failed to fetch previews: {str(e)}'}, 
            status=500
        )
    
