from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_POST
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

from .serializers import LoginSerializer, SignUpSerializer
from .models import FavJunction, Anime
from .serializers import AnimeSerializer
from django.shortcuts import get_object_or_404

def home(request):
    return render(request, 'home.html')

@api_view(['POST'])
@ensure_csrf_cookie
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        return Response({
            'success': True,
            'message': 'Login successful',
            'user': {
                'username': user.username,
                'email': user.email
            }
        })
    return Response({
        'success': False,
        'error': 'Invalid credentials'
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def signUp(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True, "message": "User created successfully"}, status = status.HTTP_201_CREATED)
    return Response({"success": False, "errorMessage": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home')  
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# @csrf_exempt
# @require_POST
# def login_view(request):
#     data = json.loads(request.body)
#     user = authenticate(request, username=data['username'], password=data['password'])
#     if user is not None:
#         login(request, user)
#         return JsonResponse({"message": "Login successful"})
#     return JsonResponse({"error": "Invalid credentials"}, status=401)

@api_view(['POST'])
@ensure_csrf_cookie
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return Response({'message': 'Successfully logged out'})
    return Response({'error': 'Not logged in'}, status=400)

@api_view(['GET'])
@ensure_csrf_cookie
def whoami_view(request):
    if request.user.is_authenticated:
        return Response({
            "username": request.user.username,
            "email": request.user.email,
        })
    return Response({"error": "Not authenticated"}, status=401)

@api_view(['GET'])
def get_user_favorites(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Not authenticated'}, status=401)
    
    # Get all favorite anime for the current user
    favorite_anime = Anime.objects.filter(favorited_by__user=request.user)
    serializer = AnimeSerializer(favorite_anime, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@ensure_csrf_cookie
def add_to_favorites(request, anime_id):
    if not request.user.is_authenticated:
        return Response({'error': 'Not authenticated'}, status=401)
    
    try:
        # Validate required fields
        required_fields = ['name', 'imageURL']
        for field in required_fields:
            if not request.data.get(field):
                return Response(
                    {'error': f'Missing required field: {field}'}, 
                    status=400
                )

        # Convert rating to integer with fallback
        try:
            rating = int(request.data.get('rating', 0))
        except (ValueError, TypeError):
            rating = 0

        # First, create or update the anime entry
        anime, created = Anime.objects.update_or_create(
            id=anime_id,
            defaults={
                'name': request.data.get('name', ''),
                'description': request.data.get('description', ''),
                'imageURL': request.data.get('imageURL', ''),
                'releaseDate': request.data.get('releaseDate') or None,
                'genre': request.data.get('genre', ''),
                'rating': rating,
                'characters': request.data.get('characters', '')
            }
        )

        # Then create the favorite relationship
        favorite, created = FavJunction.objects.get_or_create(
            user=request.user,
            anime=anime
        )

        return Response({
            'message': 'Added to favorites',
            'created': created
        })

    except Exception as e:
        return Response({
            'error': str(e),
            'details': 'Failed to add anime to favorites'
        }, status=400)

@api_view(['DELETE'])
def remove_from_favorites(request, anime_id):
    if not request.user.is_authenticated:
        return Response({'error': 'Not authenticated'}, status=401)
    
    favorite = get_object_or_404(FavJunction, user=request.user, anime_id=anime_id)
    favorite.delete()
    return Response({'message': 'Removed from favorites'})


