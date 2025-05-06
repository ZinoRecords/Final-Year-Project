from django.test import TestCase

import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework import status
from .models import Anime, FavJunction
from django.contrib.auth import get_user_model



User = get_user_model()

class AuthViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = "testuser"
        self.password = "testpass123"
        self.email = "test@example.com"
        self.user = User.objects.create_user(username=self.username, password=self.password, email=self.email)

    def test_SuccessfulSignup(self):
        response = self.client.post("/app/signUp/", data=json.dumps({
            "username": "aUniqueUser",
            "password": "passwd",
            "email": "uniqueEmail@example.com"
        }), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_UsernameInUse(self):
        response = self.client.post("/app/signUp/", data=json.dumps({
            "username": self.username,
            "password": "passwd",
            "email": "anotherUniqueEmail@example.com"
        }), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_EmailInUse(self):
        response = self.client.post("/app/signUp/", data=json.dumps({
            "username": "uniqueUser2",
            "password": "passwd",
            "email": self.email  # same as the one from setUp
        }), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_LoginSuccessfully(self):
        response = self.client.post("/app/login/", data=json.dumps({
            "username": self.username,
            "password": self.password
        }), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_LoginWrongPassword(self):
        response = self.client.post("/app/login/", data=json.dumps({
            "username": self.username,
            "password": "wrongPassword"
        }), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_LoginUsernameNotFound(self):
        response = self.client.post("/app/login/", data=json.dumps({
            "username": "fakeUser",
            "password": "passwd"
        }), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_Logout(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post("/app/logout/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_whoamiAuthenticated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get("/app/whoami/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_whoamiUnauthenticated(self):
        response = self.client.get("/app/whoami/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class FavoriteViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="username", password="passwd")
        self.anime_data = {
            "id": 12345,
            "name": "Test Anime",
            "description": "A great anime",
            "imageURL": "http://example.com/image.jpg",
            "releaseDate": "2021-01-01",
            "genre": ["Action", "Adventure"],
            "rating": 8.5,
            "characters": []
        }

    def test_AddToFavorites(self):
        self.client.login(username="username", password="passwd")
        response = self.client.post("/app/favorites/add/", data=json.dumps(self.anime_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_RemoveFavorites(self):
        self.client.login(username="username", password="passwd")
        anime = Anime.objects.create(**self.anime_data)
        FavJunction.objects.create(user=self.user, anime=anime)
        response = self.client.delete("/app/favorites/remove/", data=json.dumps({"name": "Test Anime"}), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_GetUserFavorites(self):
        self.client.login(username="username", password="passwd")
        anime = Anime.objects.create(**self.anime_data)
        FavJunction.objects.create(user=self.user, anime=anime)
        response = self.client.get("/app/favorites/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    

