from django.urls import path
from .views import register_user, login_user, profile_view

urlpatterns = [
    path('profile/', profile_view, name='profile'),
]
