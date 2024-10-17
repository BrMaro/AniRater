from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login, logout
from django.db.utils import IntegrityError

# Registration view
@api_view(['POST'])
def register_user(request):
    print("Registering")
    data = request.data
    
    # Check for missing fields
    if not all(key in data for key in ('username', 'email', 'password')):
        return Response({"error": "All fields (username, email, password) are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Check for existing user
        if User.objects.filter(username=data['username']).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=data['email']).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Create user
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        user.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    except IntegrityError:
        return Response({"error": "Database error occurred. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Login view
@api_view(['POST'])
def login_user(request):
    print("Logging in")
    data = request.data
    
    # Check for missing fields
    if not all(key in data for key in ('username', 'password')):
        return Response({"error": "Both username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
    
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
        try:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": f"An error occurred while fetching profile: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"error": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
