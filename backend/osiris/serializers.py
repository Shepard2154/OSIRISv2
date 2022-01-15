from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import TwitterUserInfo, TwitterTweet


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterUserInfo
        fields = ['id', 'screen_name', 'name']


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterUserInfo
        fields = ['id', 'screen_name', 'name']


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterUserInfo
        fields = ['id', 'screen_name', 'name']

class TweetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterTweet
        fields = ['id', 'created_at', 'text']

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

class LoginSerializer(serializers.Serializer):
    """
    Authenticates an existing user.
    Email and password are required.
    Returns a JSON web token.
    """
    username = serializers.CharField(max_length=50, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    # Ignore these fields if they are included in the request.
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        """
        Validates user data.
        """
        username = data.get('username', None)
        password = data.get('password', None)

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
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

        return {
            'token': user.csrfmiddlewaretoken,
        }