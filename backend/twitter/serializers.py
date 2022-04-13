from rest_framework import serializers

from .models import (
    TwitterUser, 
    TwitterTweet,
)


class TweetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterTweet
        fields = '__all__'


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    screen_name = serializers.CharField()
    name = serializers.CharField()
    twitter_url = serializers.CharField()
    profile_image_url = serializers.CharField(allow_blank=True)
    description = serializers.CharField(allow_blank=True)
    hashtags = serializers.JSONField(allow_null=True)
    birthday = serializers.DateTimeField()
    created = serializers.DateTimeField()
    web = serializers.CharField(allow_null=True)
    location = serializers.CharField(allow_blank=True)
    category = serializers.CharField(allow_null=True)
    followers_count = serializers.IntegerField()
    friends_count = serializers.IntegerField()
    likes_count = serializers.IntegerField()
    statuses_count = serializers.IntegerField()
    listed_count = serializers.IntegerField()
    updated_at = serializers.DateTimeField()


    def create(self, validated_data):
        return TwitterUser.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.screen_name = validated_data.get('screen_name', instance.screen_name)
        instance.name = validated_data.get('name', instance.name)
        instance.twitter_url = validated_data.get('twitter_url', instance.twitter_url)
        instance.profile_image_url = validated_data.get('profile_image_url', instance.profile_image_url)
        instance.description = validated_data.get('description', instance.description)
        instance.hashtags = validated_data.get('hashtags', instance.hashtags)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.created = validated_data.get('created', instance.created)
        instance.web = validated_data.get('web', instance.web)
        instance.location = validated_data.get('location', instance.location)
        instance.category = validated_data.get('category', instance.category)
        instance.followers_count = validated_data.get('followers_count', instance.followers_count)
        instance.friends_count = validated_data.get('friends_count', instance.friends_count)
        instance.likes_count = validated_data.get('likes_count', instance.likes_count)
        instance.statuses_count = validated_data.get('statuses_count', instance.statuses_count)
        instance.listed_count = validated_data.get('listed_count', instance.listed_count)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)       
        instance.save()
        return instance


class TweetSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created = serializers.DateTimeField()
    text = serializers.CharField()
    lang = serializers.CharField()
    source = serializers.CharField()

    author_id = serializers.IntegerField()
    author_screen_name = serializers.CharField()

    reply_count = serializers.IntegerField()
    retweet_count = serializers.IntegerField()
    quote_count = serializers.IntegerField()
    likes_count = serializers.IntegerField()

    original_screen_name = serializers.CharField(allow_blank=True)
    retweet_created = serializers.DateTimeField()
    retweet_id = serializers.IntegerField(allow_null=True)

    hashtags = serializers.JSONField(allow_null=True)
    urls = serializers.JSONField(allow_null=True)
    user_mentions = serializers.JSONField(allow_null=True)
    coordinates = serializers.JSONField(allow_null=True)

    updated_at = serializers.DateTimeField()


    def create(self, validated_data):
        return TwitterTweet.objects.create(**validated_data)
    
    
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.created = validated_data.get('created', instance.created)
        instance.text = validated_data.get('text', instance.text)
        instance.lang = validated_data.get('lang', instance.lang)
        instance.source = validated_data.get('source', instance.source)
        instance.author_id = validated_data.get('author_id', instance.author_id)
        instance.author_screen_name = validated_data.get('author_screen_name', instance.author_screen_name)
        instance.reply_count = validated_data.get('reply_count', instance.reply_count)
        instance.retweet_count = validated_data.get('retweet_count', instance.retweet_count)
        instance.quote_count = validated_data.get('quote_count', instance.quote_count)
        instance.likes_count = validated_data.get('likes_count', instance.likes_count)
        instance.original_screen_name = validated_data.get('original_screen_name', instance.original_screen_name)
        instance.retweet_created = validated_data.get('retweet_created', instance.retweet_created)
        instance.retweet_id = validated_data.get('retweet_id', instance.retweet_id)
        instance.hashtags = validated_data.get('hashtags', instance.hashtags)
        instance.urls = validated_data.get('urls', instance.urls)
        instance.user_mentions = validated_data.get('user_mentions', instance.user_mentions)
        instance.coordinates = validated_data.get('coordinates', instance.coordinates)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)        
        instance.save()
        return instance