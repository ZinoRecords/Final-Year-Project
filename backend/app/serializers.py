from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from .models import Anime

User = get_user_model()

class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        User = get_user_model()

        username = data.get('username')
        password = data.get('password')


        # Check if username exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Incorrect username or password")

        # If user exists, check password
        if not check_password(password, user.password):
            raise serializers.ValidationError("Incorrect username or password")

        return {"user": user}

class SignUpSerializer(serializers.ModelSerializer):

    class Meta:

        model = get_user_model()
        fields = ['username','password','email']

    def validate(self, data):

        # Checks if email is already in use

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"username": "An account with this email already exists"})

        # Checks is username is already in use

        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"errorMessage": "An account with this username already exists"})
            
        return data
            
    
    def create(self, validatedData):
        
        # Create a new user in the database

        user = User.objects.create(
            username = validatedData['username'],
            email = validatedData['email']
        )
        user.set_password(validatedData['password'])
        user.save()
        return user

class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = ['id', 'name', 'description', 'imageURL', 'releaseDate', 'genre', 'rating', 'characters']
