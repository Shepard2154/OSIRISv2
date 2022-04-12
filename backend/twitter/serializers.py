from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import serializers

from .models import (
    TwitterUserInfo, 
    TwitterTweet,
    TwitterRelations,
    TwitterTweetsStatistics,
)



class TweetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterTweet
        fields = '__all__' 


class TweetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterTweet
        fields = '__all__'


class TweetListStatistics(serializers.ModelSerializer):
    class Meta:
        model = TwitterTweetsStatistics
        fields = '__all__'


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


# class TweetRetrieveSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
#     text = serializers.CharField()
#     lang = serializers.CharField()
#     retweet_count = serializers.IntegerField()
#     favorite_count = serializers.IntegerField()
#     hashtags = models.CharField(max_length=500, default=None, blank=True, null=True)
#     urls = models.CharField(max_length=500, default=None, blank=True, null=True)
#     user_mentions = models.CharField(max_length=500, default=None, blank=True, null=True)
#     coordinates = models.CharField(max_length=50, default=None, blank=True, null=True)
#     source = serializers.CharField()
#     tweet_type = serializers.CharField()
#     media = serializers.CharField()
#     original_screen_name = serializers.CharField()
#     user_id = serializers.IntegerField()
