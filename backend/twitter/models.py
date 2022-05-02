from django.db import models
from django.utils import timezone
from django_prometheus.models import ExportModelOperationsMixin


class TwitterUser(ExportModelOperationsMixin('user'), models.Model):
    id = models.BigIntegerField(primary_key=True)
    screen_name = models.CharField(max_length=250, unique=True)
    name = models.CharField(max_length=250)
    twitter_url = models.CharField(max_length=100, default='undefined', blank=True, null=True)
    profile_image_url = models.CharField(max_length=250, default='undefined', blank=True)
    description = models.CharField(max_length=2500, default='undefined', blank=True, null=True)
    hashtags = models.JSONField(null=True)
    description_urls = models.JSONField(null=True)
    birthday = models.DateTimeField()
    created = models.DateTimeField()
    web = models.CharField(max_length=300, default='undefined', blank=True, null=True)
    location = models.CharField(max_length=100, default='undefined', blank=True, null=True)
    category = models.CharField(max_length=200, default='undefined', blank=True, null=True)

    followers_count = models.BigIntegerField(default=0, blank=True, null=True)
    friends_count = models.BigIntegerField(default=0, blank=True, null=True)
    likes_count = models.BigIntegerField(default=0, blank=True, null=True)
    statuses_count = models.BigIntegerField(default=0, blank=True, null=True)
    listed_count = models.BigIntegerField(default=0, blank=True, null=True)
    
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'twitter_user'

    def __str__(self):
        return self.screen_name


class TwitterTweet(ExportModelOperationsMixin('tweet'), models.Model):
    id = models.BigIntegerField(primary_key=True)
    created = models.DateTimeField(default=timezone.now, blank=True, null=True)
    text = models.CharField(max_length=2500)
    lang = models.CharField(max_length=10)
    source = models.CharField(max_length=50)

    author_id = models.BigIntegerField(default=0)
    author_screen_name = models.CharField(max_length=50, default='')

    reply_count = models.BigIntegerField(default=0, blank=True, null=True)
    retweet_count = models.BigIntegerField(default=0, blank=True, null=True)
    quote_count = models.BigIntegerField(default=0, blank=True, null=True)
    likes_count = models.BigIntegerField(default=0, blank=True, null=True)
    original_screen_name = models.CharField(max_length=50, blank=True, null=True) # имя процитированного, ретвитнутого, отвеченного пользователя
    retweet_created = models.DateTimeField(default=timezone.now, blank=True, null=True)
    retweet_id = models.BigIntegerField(default=0, blank=True, null=True)

    hashtags = models.JSONField(null=True)
    urls = models.JSONField(null=True)
    user_mentions = models.JSONField(null=True)
    coordinates = models.JSONField(null=True)

    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.author_screen_name
    class Meta:
        db_table = 'twitter_tweet'


class TwitterRelations(ExportModelOperationsMixin('ralation'), models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(TwitterUser, db_column='user_id', on_delete=models.CASCADE)
    follower_id = models.PositiveIntegerField()
    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)

    class Meta:
        db_table = 'twitter_relations'
        unique_together = ['user_id', 'follower_id']


class TwitterHashtags(models.Model):
    id =  models.AutoField(primary_key=True)
    hashtag_value = models.CharField(max_length=100)

    class Meta:
        db_table = 'twitter_hashtags'


class TwitterPersons(models.Model):
    id =  models.AutoField(primary_key=True)
    person_screen_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'twitter_persons'


class TwitterLikes(ExportModelOperationsMixin('likes'), models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=160)
    liked_user = models.CharField(max_length=160)
    liked_user_id = models.BigIntegerField(null=True)
    tweet_text = models.CharField(max_length=300)
    tweet_hashtags = models.JSONField(null=True)
    tweet_links = models.JSONField(null=True)
    
    def __str__(self):
        return self.user

    class Meta:
        db_table = 'twitter_likes'
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class TwitterComments(ExportModelOperationsMixin('comments'), models.Model):
    id = models.BigIntegerField(primary_key=True)
    author_id = models.BigIntegerField(default=0)
    author_screen_name = models.CharField(max_length=50)
    created = models.DateTimeField()
    text = models.CharField(max_length=2500)
    hashtags = models.JSONField(null=True)
    urls = models.JSONField(null=True)
    likes_count = models.BigIntegerField(null=True)
    retweet_count = models.BigIntegerField(null=True)
    quote_count = models.BigIntegerField(null=True)
    reply_count = models.BigIntegerField(null=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.author_screen_name

    class Meta:
        db_table = 'twitter_comments'
        verbose_name = 'Комментраий'
        verbose_name_plural = 'Комментарии'

