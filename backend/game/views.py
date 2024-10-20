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

# @api_view(['GET'])
# def get_level_anime(request, level):
#     level_ranges = {
#     1: (1, 250),      # Extremely Easy
#     2: (251, 500),    # Easy
#     3: (501, 1000),   # Medium
#     4: (1001, 3000),  # Hard
#     5: (3001, 5000),  # Very Hard
#     6: (5001, 999999) # Extreme
#     }

#     if level not in level_ranges:
#         return Response()
    