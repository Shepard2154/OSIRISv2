from rest_framework import serializers

from .models import Replies, Tweets, Users, Likes


class UsersSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    screen_name = serializers.CharField()
    name = serializers.CharField(allow_blank=True)
    twitter_url = serializers.CharField()
    profile_image_url = serializers.CharField(allow_blank=True)

    description = serializers.CharField(allow_blank=True)
    hashtags = serializers.JSONField(allow_null=True)
    location = serializers.CharField(allow_blank=True)
    web = serializers.CharField(allow_null=True)
    birthday = serializers.DateTimeField()
    category = serializers.CharField(allow_null=True)

    created = serializers.DateTimeField()
    followers_count = serializers.IntegerField()
    friends_count = serializers.IntegerField()
    likes_count = serializers.IntegerField()
    statuses_count = serializers.IntegerField()
    listed_count = serializers.IntegerField()

    updated_at = serializers.DateTimeField()


    def create(self, validated_data):
        return Users.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.screen_name = validated_data.get('screen_name', instance.screen_name)
        instance.name = validated_data.get('name', instance.name)
        instance.twitter_url = validated_data.get('twitter_url', instance.twitter_url)
        instance.profile_image_url = validated_data.get('profile_image_url', instance.profile_image_url)

        instance.description = validated_data.get('description', instance.description)
        instance.hashtags = validated_data.get('hashtags', instance.hashtags)
        instance.location = validated_data.get('location', instance.location)
        instance.web = validated_data.get('web', instance.web)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.category = validated_data.get('category', instance.category)

        instance.created = validated_data.get('created', instance.created)
        instance.followers_count = validated_data.get('followers_count', instance.followers_count)
        instance.friends_count = validated_data.get('friends_count', instance.friends_count)
        instance.likes_count = validated_data.get('likes_count', instance.likes_count)
        instance.statuses_count = validated_data.get('statuses_count', instance.statuses_count)
        instance.listed_count = validated_data.get('listed_count', instance.listed_count)

        instance.updated_at = validated_data.get('updated_at', instance.updated_at)    

        instance.save()

        return instance


class TweetsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created = serializers.DateTimeField()
    text = serializers.CharField()
    lang = serializers.CharField()
    source = serializers.CharField()

    author_id = serializers.IntegerField()
    author_screen_name = serializers.CharField()

    replies_count = serializers.IntegerField(allow_null=True)
    retweets_count = serializers.IntegerField(allow_null=True)
    quotes_count = serializers.IntegerField(allow_null=True)
    likes_count = serializers.IntegerField(allow_null=True)

    source_author = serializers.CharField(allow_null=True)
    source_created = serializers.DateTimeField(allow_null=True)
    source_id = serializers.IntegerField(allow_null=True)

    hashtags = serializers.JSONField(allow_null=True)
    urls = serializers.JSONField(allow_null=True)

    updated_at = serializers.DateTimeField()


    def create(self, validated_data):
        return Tweets.objects.create(**validated_data)
    
    
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.created = validated_data.get('created', instance.created)
        instance.text = validated_data.get('text', instance.text)
        instance.lang = validated_data.get('lang', instance.lang)
        instance.source = validated_data.get('source', instance.source)

        instance.author_id = validated_data.get('author_id', instance.author_id)
        instance.author_screen_name = validated_data.get('author_screen_name', instance.author_screen_name)

        instance.replies_count = validated_data.get('replies_count', instance.replies_count)
        instance.retweets_count = validated_data.get('retweets_count', instance.retweets_count)
        instance.quotes_count = validated_data.get('quotes_count', instance.quotes_count)
        instance.likes_count = validated_data.get('likes_count', instance.likes_count)

        instance.source_author = validated_data.get('source_author', instance.source_author)
        instance.source_created = validated_data.get('source_created', instance.source_created)
        instance.source_id = validated_data.get('source_id', instance.source_id)

        instance.hashtags = validated_data.get('hashtags', instance.hashtags)
        instance.urls = validated_data.get('urls', instance.urls)

        instance.updated_at = validated_data.get('updated_at', instance.updated_at)      

        instance.save()

        return instance


class LikesSerializer(serializers.Serializer):
    profile = serializers.CharField()

    liked_text = serializers.CharField()
    hashtags = serializers.JSONField(allow_null=True)
    urls = serializers.JSONField(allow_null=True)
    liked_user = serializers.CharField()
    liked_user_id = serializers.IntegerField(allow_null=True)
   
    
    def create(self, validated_data):
        return Likes.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.profile = validated_data.get('profile', instance.profile)

        instance.liked_text = validated_data.get('liked_text', instance.liked_text)
        instance.liked_user = validated_data.get('liked_user', instance.liked_user)
        instance.hashtags = validated_data.get('tweet_hashtags', instance.hashtags)
        instance.urls = validated_data.get('urls', instance.urls)       
        instance.liked_user_id = validated_data.get('liked_user_id', instance.liked_user_id)
        return instance


class RepliesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    author_id = serializers.IntegerField()
    author_screen_name = serializers.CharField()
    created = serializers.DateTimeField()

    text = serializers.CharField()
    hashtags = serializers.JSONField(allow_null=True)
    urls = serializers.JSONField(allow_null=True)

    replies_count = serializers.IntegerField()
    retweets_count = serializers.IntegerField()
    quotes_count = serializers.IntegerField(allow_null=True)
    likes_count = serializers.IntegerField()

    updated_at = serializers.DateTimeField()


    def create(self, validated_data):
        return Replies.objects.create(**validated_data)
    
    
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.author_id = validated_data.get('author_id', instance.author_id)
        instance.author_screen_name = validated_data.get('author_screen_name', instance.author_screen_name)
        instance.created = validated_data.get('created', instance.created)

        instance.text = validated_data.get('text', instance.text)
        instance.hashtags = validated_data.get('hashtags', instance.hashtags)
        instance.urls = validated_data.get('urls', instance.urls)

        instance.replies_count = validated_data.get('replies_count', instance.replies_count)
        instance.retweets_count = validated_data.get('retweets_count', instance.retweets_count)
        instance.quotes_count = validated_data.get('quotes_count', instance.quotes_count)
        instance.likes_count = validated_data.get('likes_count', instance.likes_count)

        instance.updated_at = validated_data.get('updated_at', instance.updated_at)  

        instance.save()

        return instance


class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class TweetsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweets
        fields = '__all__'


class RepliesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Replies
        fields = '__all__'