import os
import twitter
from datetime import datetime

import tweepy
from dotenv import load_dotenv
from loguru import logger

from .models import (
    TwitterUser,
    TwitterTweet
)
from .utils.getters import (
    get_hashtags,
    get_urls,
    get_user_mentions,
    get_media_url,
)
from .statistics import (
    calculate_tweets_type,
    get_domain_count,
    get_tweet_time_of_weekdays,
    get_tweet_weekday,
    get_tweet_dates,
    get_tweet_retweet_screen_name,
    get_tweet_quote_screen_name,
    get_source_count,
    get_lang_count,
    calculate_user_mentions,
    calculate_hashtags,
    calculate_network_activity,
    calculate_day_tweets,
)


logger.add("logs/services.log", format="{time} {message}", level="DEBUG", rotation="500 MB", compression="zip", encoding='utf-8')

load_dotenv()

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_key = os.getenv('ACCESS_KEY')
access_secret = os.getenv('ACCESS_SECRET')


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


def v1_get_tweet_by_id(id):
    tweet = api.get_status(id=id)
    return tweet

def get_user_info(screen_name):
    user = api.get_user(screen_name=screen_name)

    location = 'undefined'
    url = 'undefined'
    description = 'undefined'
    profile_image_url = 'undefined'

    if user.location:
        location = user.location
    if user.url:
        url = user.url
    if user.description:
        description = user.description
    if user.profile_image_url:
        profile_image_url = user.profile_image_url

    return user._json
    # user = TwitterUser(
    #     id = user.id,
    #     screen_name = user.screen_name,
    #     name = user.name,
    #     profile_image_url = profile_image_url,
    #     description = description,
    #     created_at = user.created_at,
    #     url = url,
    #     location = location,
    #     followers_count = user.followers_count,
    #     friends_count = user.friends_count,
    #     favourites_count = user.favourites_count,
    #     statuses_count = user.statuses_count,
    #     listed_count = user.listed_count,
    #     is_protected = user.protected,
    #     is_verified = user.verified,
    #     updated_at = datetime.now()
    # )
    # user.save()


def save_tweets(tweets):
    logger.debug(f"downloaded {len(tweets)}")
    for tweet in tweets:
        coordinates = 'undefined'
        if tweet.coordinates:
            coordinates = tweet.coordinates.get('coordinates')

        tweet_type_info = define_tweet_type(tweet)
        if not tweet_type_info:
            break

        tweet = TwitterTweet(
            id = tweet.id,
            created_at = tweet.created_at,
            text = tweet.full_text.replace('"', ''),
            lang = tweet.lang,
            retweet_count = tweet.retweet_count,
            favorite_count = tweet.favorite_count,
            hashtags = get_hashtags(tweet).replace('"', ''),
            urls = get_urls(tweet).replace('"', ''),
            user_mentions = get_user_mentions(tweet).replace('"', ''),
            coordinates = coordinates,
            source = tweet.source,
            tweet_type = tweet_type_info.get('tweet_type'),
            media = get_media_url(tweet).replace('"', ''),
            original_screen_name = tweet_type_info.get('original_screen_name'),
            user_id = TwitterUser.objects.get(pk=tweet.user.id)
        )

        try:
            TwitterTweet.objects.get(pk=tweet.id)  
        except twitter.models.TwitterTweet.DoesNotExist:
            tweet.save()


def download_all_tweets(screen_name):
    tweets = []
    current_tweets = []
    
    try:
        current_tweets = api.user_timeline(
            screen_name=screen_name, 
            count=200, 
            tweet_mode='extended'
        )
    except tweepy.errors.Unauthorized:
        return tweets

    tweets.extend(current_tweets)
    oldest_id = tweets[-1].id

    while True:
        current_tweets = api.user_timeline(
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


def get_tweets_statistics(screen_name):
    pass
    # user_id = TwitterUser.objects.get(screen_name=screen_name).id

    # created_at_values = TwitterTweet.objects.values_list('created_at', flat=True).filter(user_id=user_id)
    # weekdays_time_activity = get_tweet_time_of_weekdays(created_at_values)
    # week_activity = get_tweet_weekday(created_at_values)
    # date_activity = get_tweet_dates(created_at_values)

    # langs_values = TwitterTweet.objects.values_list('lang', flat=True).filter(user_id=user_id)
    # langs = get_lang_count(langs_values)

    # devices_values = TwitterTweet.objects.values_list('source', flat=True).filter(user_id=user_id)
    # devices = get_source_count(devices_values)

    # urls_mentions_values = TwitterTweet.objects.values_list('urls', flat=True).filter(user_id=user_id)
    # url_mentions = get_domain_count(urls_mentions_values)

    # user_mentions_values = TwitterTweet.objects.values_list('user_mentions', flat=True).filter(user_id=user_id)
    # user_mentions = calculate_user_mentions(user_mentions_values)

    # hashtags_values = TwitterTweet.objects.values_list('hashtags', flat=True).filter(user_id=user_id)
    # hashtags = calculate_hashtags(hashtags_values)

    # type_tweets_values = TwitterTweet.objects.values_list('tweet_type', flat=True).filter(user_id=user_id)
    # type_tweets = calculate_tweets_type(type_tweets_values)

    # quotes_values = type_tweets_values.filter(tweet_type='Цитата')
    # quotes = quotes_values.values_list('original_screen_name')
    # quotes_count = get_tweet_quote_screen_name(quotes)

    # retweets_values = type_tweets_values.filter(tweet_type='Ретвит')
    # retweets = retweets_values.values_list('original_screen_name')
    # retweets_count = get_tweet_quote_screen_name(retweets)

    # TwitterTweetsStatistics(
    #     user_id=user_id,
    #     week_time_activity= models.JSONField()
    #     date_activity= models.JSONField()
    #     week_activity= models.JSONField()
    #     devices= models.JSONField()
    #     url_mentions= models.JSONField(null=True)
    #     user_mentions= models.JSONField(null=True)
    #     hashtags= models.JSONField(null=True)
    #     quotes= models.JSONField(null=True)
    #     type_tweets= models.JSONField()
    #     retweets= 
    # )


def define_tweet_type(tweet):
    quote_screen_name = ''
    retweet_screen_name = ''
    
    try: quote_screen_name = api.get_status(id=tweet.quoted_status_id).user.screen_name
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