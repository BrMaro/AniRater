"""
URL configuration for AniRater project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users.views import register_user,login_user,check_auth
from game.views import random_anime,get_level_previews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path("check-auth/",check_auth, name="check-auth"),
    path('api/level-previews/<int:level>/', get_level_previews, name='level_previews'),
    path('api/random-anime/<int:difficulty>/', random_anime, name='random_anime'),
]
