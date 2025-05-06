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
    else:
        return Response({
        'success': False,
        'error': 'Invalid credentials'
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@ensure_csrf_cookie
def signUp(request):

    serializer = SignUpSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user is not None:
            login(request, user)
        return Response({"success": True, "message": "User created successfully"}, status = status.HTTP_201_CREATED)

    return Response({"success": False, "errorMessage": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@ensure_csrf_cookie
def logout_view(request):

    if request.user.is_authenticated:
        logout(request)
        return Response({'message': 'Successfully logged out'})

    return Response({'error': 'Not logged in'}, status=400)

@api_view(['GET'])
@ensure_csrf_cookie
# Gets the current logged in users username and email
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
    
    # Get all favourite animes for the logged in user
    favouriteAnimes = Anime.objects.filter(favorited_by__user=request.user)
    serializer = AnimeSerializer(favouriteAnimes, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_to_favorites(request):

    if not request.user.is_authenticated:
        return Response({'error': 'Not authenticated'}, status=401)
 
    data = request.data

    releaseDate = data['releaseDate']
    # Jikan gives year of release as int, so we convert it to str
    if isinstance(releaseDate, int):
        releaseDate = str(releaseDate)

    if len(releaseDate) == 4:
        releaseDate = f"{releaseDate}-01-01"

    # If the animes not in the database then it adds it
    anime, created = Anime.objects.get_or_create(
        id=data['id'],
        defaults={
            'name': data['name'],
            'description': data['description'],
            'imageURL': data['imageURL'],
            'releaseDate': releaseDate,
            'genre': data['genre'],
            'rating': data['rating'],
            'characters': data['characters']
        }
    )

    favorite, favCreated = FavJunction.objects.get_or_create(user=request.user, anime=anime)

    # Displayed in console for debugging
    if favCreated:
        return Response({'message': f'Anime "{anime.name}" added to favorites.'}, status=201)
    else:
        return Response({'message': f'Anime "{anime.name}" is already in favorites.'}, status=200)
    
    



@api_view(['DELETE'])
def remove_from_favorites(request):

    if not request.user.is_authenticated:
        return Response({'error': 'Not authenticated'}, status=401)

    animeName = request.data.get('name')

    # If the name isn't given then return an error
    if not animeName:
        return Response({'error': 'Anime name not provided'}, status=400)

    anime = get_object_or_404(Anime, name=animeName)
    favorite = get_object_or_404(FavJunction, user=request.user, anime=anime)
    favorite.delete()

    return Response({'message': 'Removed from favorites'})


