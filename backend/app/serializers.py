from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        User = get_user_model()
        username = data.get('username')
        password = data.get('password')
        print(f'username: {username}, password: {password}')
        print(User.objects.all())


        # Retrieve the user by the provided username
        try:
            user = User.objects.get(username=username)
            print(user)
        except User.DoesNotExist:
            print('In user does not exist')
            raise serializers.ValidationError("Incorrect username or password")

        # Verify the password manually using Django's password checker
        if not check_password(password, user.password):
            print('In check password')
            raise serializers.ValidationError("Incorrect username or password")

        return {"user": user}

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username','password','email']

    def validate(self, data):

        if User.objects.filter(email=data['email']).exists():
            print('In the email checker')
            raise serializers.ValidationError({"errorMessage": "An account with this email already exists"})

        if User.objects.filter(username=data['username']).exists():
            print('In the username checker')
            raise serializers.ValidationError({"errorMessage": "A user with this username already exists"})
            
        return data
            
    
    def create(self, validatedData):
        user = User.objects.create(
            username = validatedData['username'],
            email = validatedData['email']
        )
        user.set_password(validatedData['password'])
        user.save()
        return user
