import datetime as DT
import json
import re
from datetime import datetime
from dateutil.parser import parse
from pathlib import Path

import pandas as pd
import tweepy
from django.conf import settings
from django.db.utils import IntegrityError
from loguru import logger

from .models import TwitterComments, TwitterPersons, TwitterTweet, TwitterHashtags, TwitterUser
from .serializers import TweetSerializer, UserSerializer, TwitterCommentsSerializer
from .hashtags import twitter


logger.add("logs/twitter_services.log", format="{time} {message}", level="DEBUG", rotation="500 MB", compression="zip", encoding='utf-8')


def get_hashtags_from_file():
    BASE_DIR = Path(__file__).resolve().parent.parent
    hashtags_df = pd.read_excel('static/hashtags.xlsx', usecols=[0,2,4,6,8], na_filter=False)
    hashtags_df.dropna(inplace=True)
    hashtags = hashtags_df.to_dict('list')

    all_hashtags = []
    for hashtag_class in hashtags:
        all_hashtags.extend([hashtag_item[1:] for hashtag_item in hashtags.get(hashtag_class) if hashtag_item])
    all_hashtags = list(set(all_hashtags))

    for hashtag in all_hashtags:
        TwitterHashtags.objects.update_or_create(hashtag_value=hashtag)
    return all_hashtags


def from_v2_tweet(tweet):
    urls = []
    if tweet.get('outlinks'):
        urls += tweet.get('outlinks')
        if tweet.get('tcooutlinks'):
            urls += tweet.get('tcooutlinks')

    id = tweet.get('id')
    created = tweet.get('date')
    text = tweet.get('content')
    lang = tweet.get('lang')
    source = tweet.get('sourceLabel')

    author_id = tweet.get('user').get('id')
    author_screen_name = tweet.get('user').get('username')

    reply_count = tweet.get('replyCount')
    retweet_count = tweet.get('retweetCount')
    quote_count = tweet.get('quoteCount')
    likes_count = tweet.get('likeCount')

    original_screen_name = tweet.get('inReplyToUser').get('username') if tweet.get('inReplyToUser') else ''
    retweet_created = datetime(2006, 3, 1, 0, 0, 0, 0)
    retweet_id = tweet.get('inReplyToTweetId')

    hashtags = tweet.get('hashtags')
    user_mentions = tweet.get('mentionedUsers')
    coordinates = tweet.get('coordinates')

    updated_at = datetime.now()

    valid_tweet = {
        'id': id,
        'created': created,
        'text': text,
        'lang': lang,
        'source': source,
        'author_id': author_id,
        'author_screen_name': author_screen_name,
        'reply_count': reply_count,
        'retweet_count': retweet_count,
        'quote_count': quote_count,
        'likes_count': likes_count,
        'original_screen_name': original_screen_name,
        'retweet_created': retweet_created,
        'retweet_id': retweet_id,
        'hashtags': hashtags,
        'urls': urls,
        'user_mentions': user_mentions,
        'coordinates': coordinates,
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
    valid_user['description_urls'] = user.get('descriptionUrls')
    valid_user['hashtags'] = []
    valid_user['birthday'] = datetime(2006, 3, 1, 0, 0, 0, 0)
    valid_user['created'] = user.get('created')
    valid_user['web'] = user.get('linkUrl')
    valid_user['location'] = user.get('location')
    valid_user['category'] = user.get('label')
    valid_user['followers_count'] = user.get('followersCount')
    valid_user['friends_count'] = user.get('friendsCount')
    valid_user['likes_count'] = user.get('favouritesCount')
    valid_user['statuses_count'] = user.get('statusesCount')
    valid_user['listed_count'] = user.get('listedCount')
    valid_user['updated_at'] = datetime.now()

    return valid_user


def v2_download_tweets_by_hashtag(hashtag_item):
    scraper = twitter.TwitterHashtagScraper(hashtag_item)
    for tweet in scraper.get_items():
        if int(settings.REDIS_INSTANCE.get(hashtag_item)):
            valid_tweet = from_v2_tweet(json.loads(tweet.json()))
            serializer = TweetSerializer(data=valid_tweet)
            serializer.is_valid(raise_exception=True)
            try:
                serializer.save()
                logger.info(f"Этот твит ({serializer.data.get('id')}) только что был добавлен в Базу Данных!")
            except IntegrityError:
                logger.warning(f"Этот твит ({serializer.data.get('id')}) уже содержится в Базе Данных!")
                serializer.update(TwitterTweet.objects.get(pk=serializer.data.get('id')), serializer.validated_data)
        else:
            break


def download_tweets_by_hashtag(hashtag_item):
    scraper = twitter.TwitterHashtagScraper(hashtag_item)

    for tweet in scraper.get_items():
        yield json.loads(tweet.json())
        if not int(settings.REDIS_INSTANCE.get(hashtag_item)):
            break


def download_username(username):
    scraper = twitter.TwitterUserScraper(username)
    user = scraper._get_entity()
    return user


def v2_download_username(username):
    if int(settings.REDIS_INSTANCE.get(username)):
        scraper = twitter.TwitterUserScraper(username)
        user = scraper._get_entity()

        valid_user = from_v2_user(user)
        serializer = UserSerializer(data=valid_user)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            logger.info(f"Этот пользователь ({serializer.data.get('screen_name')}) только что был добавлен в Базу Данных!")
        except IntegrityError:
            logger.warning(f"Этот пользователь ({serializer.data.get('screen_name')}) уже содержится в Базе Данных!")
            serializer.update(TwitterUser.objects.get(pk=serializer.data.get('id')), serializer.validated_data)
        return user


def v1_get_tweet_by_id(id):
    tweet = settings.TWITTER_APIV1.get_status(id=id)
    return tweet


def get_user_info(screen_name):
    user = settings.TWITTER_APIV1.get_user(screen_name=screen_name)._json
    return user


def from_v1_user(v1_user):
    valid_user = {}
    valid_user['id'] = v1_user.get('id')
    valid_user['screen_name'] = v1_user.get('screen_name')
    valid_user['name'] = v1_user.get('name')
    valid_user['twitter_url'] = f"https://twitter.com/{valid_user.get('screen_name')}"
    valid_user['profile_image_url'] = v1_user.get('profile_image_url')
    valid_user['description'] = v1_user.get('description')
    valid_user['description_urls'] = v1_user.get('entities').get('description').get('urls')
    valid_user['hashtags'] = []
    valid_user['birthday'] = datetime(2006, 3, 1, 0, 0, 0, 0)
    valid_user['created'] = parse(v1_user.get('created_at'))
    valid_user['web'] = v1_user.get('url')
    valid_user['location'] = v1_user.get('location')
    valid_user['category'] = None
    valid_user['followers_count'] = v1_user.get('followers_count')
    valid_user['friends_count'] = v1_user.get('friends_count')
    valid_user['likes_count'] = v1_user.get('favourites_count')
    valid_user['statuses_count'] = v1_user.get('statuses_count')
    valid_user['listed_count'] = v1_user.get('listed_count')
    valid_user['updated_at'] = datetime.now()

    return valid_user


def from_v1_tweet(v1_tweet):
    v1_tweet = v1_tweet._json

    retweeted_status = v1_tweet.get('retweeted_status')
    quoted_status = v1_tweet.get('quoted_status')

    valid_tweet = {}
    valid_tweet['id'] = v1_tweet.get('id')
    valid_tweet['created'] = parse(v1_tweet.get('created_at'))
    valid_tweet['text'] = v1_tweet.get('full_text')
    valid_tweet['lang'] = v1_tweet.get('lang')
    valid_tweet['source'] = v1_tweet.get('source')
    valid_tweet['author_id'] = v1_tweet.get('user').get('id')
    valid_tweet['author_screen_name'] = v1_tweet.get('user').get('screen_name')
    valid_tweet['reply_count'] = v1_tweet.get('')
    valid_tweet['retweet_count'] = v1_tweet.get('retweet_count')
    valid_tweet['quote_count'] = None
    valid_tweet['likes_count'] = v1_tweet.get('favorite_count')
    valid_tweet['original_screen_name'] = v1_tweet.get('in_reply_to_screen_name')
    valid_tweet['retweet_created'] = retweeted_status.get('created_at') if retweeted_status else None
    valid_tweet['retweet_id'] = retweeted_status.get('id') if retweeted_status else None
    valid_tweet['hashtags'] = v1_tweet.get('entities').get('hashtags')
    valid_tweet['urls'] = v1_tweet.get('entities').get('urls')
    valid_tweet['user_mentions'] = v1_tweet.get('entities').get('user_mentions')
    valid_tweet['coordinates'] = v1_tweet.get('coordinates')
    valid_tweet['updated_at'] = datetime.now()
    
    return valid_tweet


def define_tweet_type(tweet):
    quote_screen_name = ''
    retweet_screen_name = ''
    
    try: quote_screen_name = settings.TWITTER_APIV1.get_status(id=tweet.quoted_status_id).user.screen_name
    except Exception: pass

    try: retweet_screen_name = tweet.retweeted_status.user.screen_name
    except Exception: pass
    
    if not quote_screen_name and not retweet_screen_name:
        return {'tweet_type': 'Твит', 'original_screen_name': ''}
    elif quote_screen_name and not retweet_screen_name :
        return {'tweet_type': 'Цитата', 'original_screen_name': quote_screen_name}
    elif not quote_screen_name and retweet_screen_name:
        return {'tweet_type': 'Ретвит', 'original_screen_name': retweet_screen_name}
    else:
        # нештатная ситуация
        return {'tweet_type': 'Не определено', 'original_screen_name': f'q:{quote_screen_name}|r:{retweet_screen_name}'}


def download_all_tweets(screen_name):
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


def v1_get_likes_user(screen_name):
  tweet_list=settings.TWITTER_APIV1.get_favorites(screen_name=screen_name, count=200)
  likes = []
  for i in tweet_list:
    likes.append({'user': screen_name, 'liked_user': i.user.screen_name, 'liked_user_id': i.user.id, 'tweet_text': i.text , 'tweet_hashtags': re.findall(r'(#\w+)', i.text), 'tweet_links': re.findall("(?P<url>https?://[^\s]+)", i.text)})
  return likes


def v2_get_comments(screen_name, max_count=200):
    comments_count = 0
    for comment in twitter.TwitterSearchScraper(f'from:{screen_name} filter:replies').get_items():
        valid_tweet = from_v2_tweet(comment)
        serializer = TwitterCommentsSerializer(data=valid_tweet)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
            logger.info(f"Этот комментарий ({serializer.data.get('id')}) только что был добавлен в Базу Данных!")
        except IntegrityError:
            logger.warning(f"Этот комментарий ({serializer.data.get('id')}) уже содержится в Базе Данных!")
            serializer.update(TwitterComments.objects.get(pk=serializer.data.get('id')), serializer.validated_data)

        comments_count += 1
        if comments_count >= max_count:
            break