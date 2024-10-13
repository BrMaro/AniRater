from django.urls import path
from .views import random_anime

urlpatterns = [
    path('api/random-anime/<int:difficulty>/', random_anime, name='random_anime'),
]