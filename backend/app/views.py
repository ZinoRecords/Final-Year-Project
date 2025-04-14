from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import LoginSerializer, SignUpSerializer
from rest_framework.decorators import api_view


def home(request):
    return render(request, 'home.html')

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response({"success": True}, status=status.HTTP_200_OK)

    return Response({"success": False, "error": serializer.errors})

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


@csrf_protect
@require_POST
def login_view(request):
    data = json.loads(request.body)
    user = authenticate(request, username=data['username'], password=data['password'])
    if user is not None:
        login(request, user)
        return JsonResponse({"message": "Login successful"})
    return JsonResponse({"error": "Invalid credentials"}, status=401)

@require_POST
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logged out"})

@login_required
def whoami_view(request):
    return JsonResponse({
        "username": request.user.username,
        "id": request.user.id,
        "email": request.user.email,
    })
            

