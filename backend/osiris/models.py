from django.db import models
from django.utils import timezone  


class TwitterUserInfo(models.Model):
    id = models.BigIntegerField(primary_key=True)
    screen_name = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    profile_image_url = models.CharField(max_length=100, default='undefined', blank=True)
    description = models.CharField(max_length=160, default='undefined', blank=True, null=True)
    created_at = models.DateTimeField()
    url = models.CharField(max_length=50, default='undefined', blank=True, null=True)
    location = models.CharField(max_length=50, default='undefined', blank=True, null=True)
    followers_count = models.BigIntegerField(default=0, blank=True, null=True)
    friends_count = models.BigIntegerField(default=0, blank=True, null=True)
    favourites_count = models.BigIntegerField(default=0, blank=True, null=True)
    statuses_count = models.BigIntegerField(default=0, blank=True, null=True)
    listed_count = models.BigIntegerField(default=0, blank=True, null=True)
    is_protected = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'twitter_userInfo'

    def __str__(self):
        return self.id


class TwitterTweet(models.Model):
    id = models.BigIntegerField(primary_key=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    text = models.CharField(max_length=500)
    lang = models.CharField(max_length=10)
    retweet_count = models.BigIntegerField(default=0, blank=True, null=True)
    favorite_count = models.BigIntegerField(default=0, blank=True, null=True)
    hashtags = models.CharField(max_length=500, default=None, blank=True, null=True)
    urls = models.CharField(max_length=500, default=None, blank=True, null=True)
    user_mentions = models.CharField(max_length=500, default=None, blank=True, null=True)
    coordinates = models.CharField(max_length=50, default=None, blank=True, null=True)
    source = models.CharField(max_length=50)
    tweet_type = models.CharField(max_length=30)
    media = models.CharField(max_length=500, default=None, blank=True, null=True)
    original_screen_name = models.CharField(max_length=50, blank=True, null=True) # имя процитированного, ретвитнутого, отвеченного пользователя
    user_id = models.ForeignKey(TwitterUserInfo, db_column='user_id', on_delete=models.CASCADE)

    class Meta:
        db_table = 'twitter_tweet'


class TwitterRelations(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(TwitterUserInfo, db_column='user_id', on_delete=models.CASCADE)
    follower_id = models.PositiveIntegerField()

    class Meta:
        db_table = 'twitter_relations'
        unique_together = ['user_id', 'follower_id']

# hints:
# число цитат можно определить по числу ссылок на twitter.com