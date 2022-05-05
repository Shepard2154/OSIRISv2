import datetime
import re
from dateutil.parser import parse
from pathlib import Path

import pandas as pd
import tweepy
from django.conf import settings
from django.db.utils import IntegrityError
from loguru import logger

from .models import Replies, Tweets, Hashtags, Users
from .serializers import TweetsSerializer, UsersSerializer, RepliesSerializer
from .hashtags import twitter


logger.add("static/logs/special_services.log", format="{time} {message}", level="INFO", rotation="500 MB", compression="zip", encoding='utf-8')


def v2_download_tweets_by_hashtag(hashtag_item):
    scraper = twitter.TwitterHashtagScraper(hashtag_item)

    for tweet in scraper.get_items():
        if int(settings.REDIS_INSTANCE.get(hashtag_item)):
            tweet_to_save = from_v2_tweet(tweet)
            serializer = TweetsSerializer(data=tweet_to_save)
            serializer.is_valid(raise_exception=True)

            try:
                serializer.save()
                logger.info(f"Этот твит ({serializer.data.get('id')}) только что был добавлен в Базу Данных!")
            except IntegrityError:
                logger.warning(f"Этот твит ({serializer.data.get('id')}) уже содержится в Базе Данных!")
                serializer.update(Tweets.objects.get(pk=serializer.data.get('id')), serializer.validated_data)
                
        else: break


def v2_download_user(screen_name):
    if settings.REDIS_INSTANCE.get(screen_name):
        user = v2_get_user(screen_name)
        valid_user = from_v2_user(user)
        serializer = UsersSerializer(data=valid_user)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
            logger.info(f"Этот пользователь ({serializer.data.get('screen_name')}) только что был добавлен в Базу Данных!")
        except IntegrityError:
            logger.warning(f"Этот пользователь ({serializer.data.get('screen_name')}) уже содержится в Базе Данных!")
            serializer.update(Users.objects.get(pk=serializer.data.get('id')), serializer.validated_data)


def v2_get_user(screen_name):
    scraper = twitter.TwitterUserScraper(screen_name)
    user = scraper._get_entity()

    return user


def from_v2_tweet(tweet):
    id = tweet.get('id')
    created = tweet.get('date')
    text = tweet.get('content')
    lang = tweet.get('lang')
    source = tweet.get('sourceLabel')

    author_id = tweet.get('user').get('id')
    author_screen_name = tweet.get('user').get('username')

    replies_count = tweet.get('replyCount')
    retweets_count = tweet.get('retweetCount')
    quotes_count = tweet.get('quoteCount')
    likes_count = tweet.get('likeCount')

    source_author = tweet.get('inReplyToUser').get('username') if tweet.get('inReplyToUser') else None
    source_created = datetime.datetime(2006, 3, 1, 0, 0, 0, 0)
    source_id = tweet.get('inReplyToTweetId')

    hashtags = tweet.get('hashtags')
    urls = []
    if tweet.get('outlinks'):
        urls += tweet.get('outlinks')
        if tweet.get('tcooutlinks'):
            urls += tweet.get('tcooutlinks')

    updated_at = datetime.datetime.now()

    valid_tweet = {
        'id': id,
        'created': created,
        'text': text,
        'lang': lang,
        'source': source,

        'author_id': author_id,
        'author_screen_name': author_screen_name,

        'replies_count': replies_count,
        'retweets_count': retweets_count,
        'quotes_count': quotes_count,
        'likes_count': likes_count,

        'source_author': source_author,
        'source_created': source_created,
        'source_id': source_id,

        'hashtags': hashtags,
        'urls': urls,

        'updated_at': updated_at
    }

    return valid_tweet


def from_v2_user(user):
    valid_user = {}
    valid_user['id'] = user.get('id')
    valid_user['screen_name'] = user.get('username')
    valid_user['name'] = user.get('displayname')
    valid_user['twitter_url'] = f"https://twitter.com/{valid_user.get('screen_name')}"
    valid_user['profile_image_url'] = user.get('profileImageUrl')

    valid_user['description'] = user.get('description')
    valid_user['hashtags'] = []
    valid_user['location'] = user.get('location')
    valid_user['web'] = user.get('linkUrl')
    valid_user['birthday'] = datetime.datetime(2006, 3, 1, 0, 0, 0, 0)
    valid_user['category'] = user.get('label')

    valid_user['created'] = user.get('created')
    valid_user['followers_count'] = user.get('followersCount')
    valid_user['friends_count'] = user.get('friendsCount')
    valid_user['likes_count'] = user.get('favouritesCount')
    valid_user['statuses_count'] = user.get('statusesCount')
    valid_user['listed_count'] = user.get('listedCount')

    valid_user['updated_at'] = datetime.datetime.now()

    return valid_user


def v1_get_tweets(screen_name):
    tweets = []
    current_tweets = []
    
    try:
        current_tweets = settings.TWITTER_APIV1.user_timeline(
            screen_name=screen_name, 
            count=200, 
            tweet_mode='extended'
        )
    except tweepy.errors.Unauthorized:
        return tweets

    tweets.extend(current_tweets)
    oldest_id = tweets[-1].id

    while True:
        current_tweets = settings.TWITTER_APIV1.user_timeline(
            screen_name=screen_name, 
            count=200, 
            max_id=oldest_id-1, 
            tweet_mode='extended'
        )
        
        if current_tweets:
            tweets.extend(current_tweets)
            oldest_id = current_tweets[-1].id
        else:
            return tweets


def v1_get_tweet(id):
    tweet = settings.TWITTER_APIV1.get_status(id=id)

    return tweet


def v1_get_user(screen_name):
    user = settings.TWITTER_APIV1.get_user(screen_name=screen_name)._json

    return user


def from_v1_tweet(tweet):
    tweet = tweet._json

    retweeted_status = tweet.get('retweeted_status')

    valid_tweet = {}
    valid_tweet['id'] = tweet.get('id')
    valid_tweet['created'] = parse(tweet.get('created_at'))
    valid_tweet['text'] = tweet.get('full_text')
    valid_tweet['lang'] = tweet.get('lang')
    valid_tweet['source'] = tweet.get('source')

    valid_tweet['author_id'] = tweet.get('user').get('id')
    valid_tweet['author_screen_name'] = tweet.get('user').get('screen_name')

    valid_tweet['replies_count'] = None
    valid_tweet['retweets_count'] = tweet.get('retweet_count')
    valid_tweet['quotes_count'] = None
    valid_tweet['likes_count'] = tweet.get('favorite_count')

    valid_tweet['source_author'] = tweet.get('in_reply_to_screen_name')
    valid_tweet['source_created'] = parse(retweeted_status.get('created_at')) if retweeted_status else None
    valid_tweet['source_id'] = retweeted_status.get('id') if retweeted_status else None

    valid_tweet['hashtags'] = tweet.get('entities').get('hashtags')
    valid_tweet['urls'] = tweet.get('entities').get('urls')

    valid_tweet['updated_at'] = datetime.datetime.now()
    
    return valid_tweet


def from_v1_user(user):
    valid_user = {}
    valid_user['id'] = user.get('id')
    valid_user['screen_name'] = user.get('screen_name')
    valid_user['name'] = user.get('name')
    valid_user['twitter_url'] = f"https://twitter.com/{valid_user.get('screen_name')}"
    valid_user['profile_image_url'] = user.get('profile_image_url')

    valid_user['description'] = user.get('description')
    valid_user['hashtags'] = []
    valid_user['location'] = user.get('location')
    valid_user['web'] = user.get('url')
    valid_user['birthday'] = datetime.datetime(2006, 3, 1, 0, 0, 0, 0)
    valid_user['category'] = None

    valid_user['created'] = parse(user.get('created_at'))
    valid_user['followers_count'] = user.get('followers_count')
    valid_user['friends_count'] = user.get('friends_count')
    valid_user['likes_count'] = user.get('favourites_count')
    valid_user['statuses_count'] = user.get('statuses_count')
    valid_user['listed_count'] = user.get('listed_count')

    valid_user['updated_at'] = datetime.datetime.now()

    return valid_user


def v1_get_likes(screen_name):
  tweets = settings.TWITTER_APIV1.get_favorites(screen_name=screen_name, count=200)

  liked_tweets = []
  for tweet in tweets:
    liked_tweets.append(
            {
                'profile': screen_name, 
                'liked_text': tweet.text,
                'hashtags': re.findall(r'(#\w+)', tweet.text), 
                'urls': re.findall("(?P<url>https?://[^\s]+)", tweet.text),
                'liked_user': tweet.user.screen_name, 
                'liked_user_id': tweet.user.id, 
            }
        )
        
  return liked_tweets


def v2_download_comments(screen_name, max_count=200):
    comments_count = 0

    for comment in twitter.TwitterSearchScraper(f'from:{screen_name} filter:replies').get_items():
        valid_tweet = from_v2_tweet(comment)
        serializer = RepliesSerializer(data=valid_tweet)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
            logger.info(f"Этот комментарий ({serializer.data.get('id')}) только что был добавлен в Базу Данных!")
        except IntegrityError:
            logger.warning(f"Этот комментарий ({serializer.data.get('id')}) уже содержится в Базе Данных!")
            serializer.update(Replies.objects.get(pk=serializer.data.get('id')), serializer.validated_data)

        comments_count += 1
        if comments_count >= max_count:
            break


def download_hashtags_from_file():
    BASE_DIR = Path(__file__).resolve().parent.parent

    hashtags_df = pd.read_excel('static/hashtags.xlsx', usecols=[0,2,4,6,8], na_filter=False)
    hashtags_df.dropna(inplace=True)
    hashtags = hashtags_df.to_dict('list')

    all_hashtags = []
    for hashtag_class in hashtags:
        all_hashtags.extend([hashtag_item[1:] for hashtag_item in hashtags.get(hashtag_class) if hashtag_item])
    all_hashtags = list(set(all_hashtags))

    for hashtag in all_hashtags:
        Hashtags.objects.update_or_create(value=hashtag)

    return all_hashtags