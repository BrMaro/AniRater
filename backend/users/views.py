from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate,login
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def register_user(request):
    # logger.info("Starting user registration process")
    data = request.data
    
    # Check for missing fields
    required_fields = ('username', 'email', 'password')
    if not all(key in data for key in required_fields):
        # logger.warning("Missing required fields in registration request")
        return Response(
            {"error": "All fields (username, email, password) are required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Check for existing username/email with better error handling
        if User.objects.filter(username=data['username']).exists():
            # logger.warning(f"Registration failed: Username '{data['username']}' already exists")
            return Response(
                {"error": "Username already exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if User.objects.filter(email=data['email']).exists():
            # logger.warning(f"Registration failed: Email '{data['email']}' already exists")
            return Response(
                {"error": "Email already exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create user
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        
        # logger.info(f"Successfully registered user: {data['username']}")
        return Response(
            {"message": "User registered successfully"}, 
            status=status.HTTP_201_CREATED
        )
        
    except IntegrityError as e:
        # logger.error(f"Database integrity error during registration: {str(e)}")
        return Response(
            {"error": "Database error occurred. Please try again later."}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        # logger.error(f"Unexpected error during registration: {str(e)}")
        return Response(
            {"error": f"An error occurred: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
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
