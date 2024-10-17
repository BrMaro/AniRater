from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login, logout


# Registration view
@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        data = request.data
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        user.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)


# Login view
@api_view(['POST'])
def login_user(request):
    data = request.data
    user = authenticate(username=data['username'], password=data['password'])
    if user is not None:
        login(request, user)
        return Response({"message": "Login successful"})
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


# Profile view
@api_view(['GET'])
def profile_view(request):
    user = request.user
    if user.is_authenticated:
        serializer = UserSerializer(user)
        return Response(serializer.data)
    else:
        return Response({"error": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
