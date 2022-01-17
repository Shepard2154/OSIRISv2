from enum import auto
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import serializers

from .models import (
    TwitterUserInfo, 
    TwitterTweet,
)


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterUserInfo
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterUserInfo
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterUserInfo
        fields = ['id', 'screen_name', 'name']


class TweetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterTweet
        fields = '__all__' 


class TweetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterTweet
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username = validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserRetrieveSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    screen_name = serializers.CharField()
    name = serializers.CharField()
    profile_image_url = serializers.CharField()
    description = serializers.CharField()
    created_at = serializers.DateTimeField()
    url = serializers.CharField()
    location = serializers.CharField()
    followers_count = serializers.IntegerField()
    friends_count = serializers.IntegerField()
    favourites_count = serializers.IntegerField()
    statuses_count = serializers.IntegerField()
    listed_count = serializers.IntegerField()
    is_protected = serializers.BooleanField()
    is_verified = serializers.BooleanField()
    updated_at = serializers.DateTimeField()

    def validate(self, data):
        return data


class LoginSerializer(serializers.Serializer):
    """
    Authenticates an existing user.
    Email and password are required.
    Returns a JSON web token.
    """
    username = serializers.CharField(max_length=50, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    csrfmiddlewaretoken = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        """
        Validates user data.
        """
        username = data.get('username', None)
        password = data.get('password', None)

        if (password is None) or (username is None):
            raise serializers.ValidationError(
                'A password and lohin are required to log in!'
            )

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        
        token = Token.objects.get_or_create(user=user)

        data['token'] = token[0].key
        data['user'] = user

        return data