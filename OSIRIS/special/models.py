from django.db import models
from django.utils import timezone
from django_prometheus.models import ExportModelOperationsMixin


class Users(ExportModelOperationsMixin('users'), models.Model):
    id = models.BigIntegerField(primary_key=True)
    screen_name = models.CharField(max_length=250, unique=True)
    name = models.CharField(max_length=250)
    twitter_url = models.CharField(max_length=100, default='', blank=True, null=True)
    profile_image_url = models.CharField(max_length=250, default='', blank=True)

    description = models.CharField(max_length=2500, default='', blank=True, null=True)
    hashtags = models.JSONField(null=True)
    location = models.CharField(max_length=100, default='', blank=True, null=True)
    web = models.CharField(max_length=300, default='', blank=True, null=True)
    birthday = models.DateTimeField()
    category = models.CharField(max_length=200, default='', blank=True, null=True)

    created = models.DateTimeField()
    followers_count = models.BigIntegerField(default=0, blank=True, null=True)
    friends_count = models.BigIntegerField(default=0, blank=True, null=True)
    likes_count = models.BigIntegerField(default=0, blank=True, null=True)
    statuses_count = models.BigIntegerField(default=0, blank=True, null=True)
    listed_count = models.BigIntegerField(default=0, blank=True, null=True)
    
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.screen_name

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Tweets(ExportModelOperationsMixin('tweets'), models.Model):
    id = models.BigIntegerField(primary_key=True)
    created = models.DateTimeField(default=timezone.now, blank=True, null=True)
    text = models.CharField(max_length=2500)
    lang = models.CharField(max_length=10)
    source = models.CharField(max_length=200)

    author_id = models.BigIntegerField(default=0)
    author_screen_name = models.CharField(max_length=200, default='')

    replies_count = models.BigIntegerField(default=0, blank=True, null=True)
    retweets_count = models.BigIntegerField(default=0, blank=True, null=True)
    quotes_count = models.BigIntegerField(default=0, blank=True, null=True)
    likes_count = models.BigIntegerField(default=0, blank=True, null=True)

    source_author = models.CharField(max_length=200, blank=True, null=True)
    source_created = models.DateTimeField(default=timezone.now, blank=True, null=True)
    source_id = models.BigIntegerField(default=0, blank=True, null=True)

    hashtags = models.JSONField(null=True)
    urls = models.JSONField(null=True)

    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.author_screen_name

    class Meta:
        db_table = 'tweets'
        verbose_name = 'Твит'
        verbose_name_plural = 'Твиты'


class Likes(ExportModelOperationsMixin('likes'), models.Model):
    number = models.AutoField(primary_key=True)

    profile = models.CharField(max_length=160)

    liked_text = models.CharField(max_length=300)
    hashtags = models.JSONField(null=True)
    urls = models.JSONField(null=True)
    liked_user = models.CharField(max_length=160)
    liked_user_id = models.BigIntegerField(null=True)
    
 
    def __str__(self):
        return self.profile

    class Meta:
        db_table = 'likes'
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class Replies(ExportModelOperationsMixin('replies'), models.Model):
    id = models.BigIntegerField(primary_key=True)
    author_id = models.BigIntegerField(default=0)
    author_screen_name = models.CharField(max_length=50)
    created = models.DateTimeField()

    text = models.CharField(max_length=2500)
    hashtags = models.JSONField(null=True)
    urls = models.JSONField(null=True)

    likes_count = models.BigIntegerField(null=True)
    retweets_count = models.BigIntegerField(null=True)
    quotes_count = models.BigIntegerField(null=True)
    replies_count = models.BigIntegerField(null=True)

    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.author_screen_name

    class Meta:
        db_table = 'replies'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Hashtags(models.Model):
    id =  models.AutoField(primary_key=True)
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.value

    class Meta:
        db_table = 'hashtags'
        verbose_name = 'хештег'
        verbose_name_plural = 'Список хештегов'


class Profiles(models.Model):
    id =  models.AutoField(primary_key=True)
    screen_name = models.CharField(max_length=100)

    def __str__(self):
        return self.screen_name

    class Meta:
        db_table = 'profiles'
        verbose_name = 'Профиль'
        verbose_name_plural = 'Список профилей'
