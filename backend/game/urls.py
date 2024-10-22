from django.urls import path
from .views import random_anime,get_level_previews,get_level_previews_async

urlpatterns = [
    path('api/random-anime/<int:difficulty>/', random_anime, name='random_anime'),
    path('api/level-previews/<int:level>/', get_level_previews),
]