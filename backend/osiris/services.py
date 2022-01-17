import datetime
import os

import tweepy
from dotenv import load_dotenv

from .models import (
    TwitterUserInfo,
)
from .utils.getters import (
    get_hashtags,
    get_urls,
    get_user_mentions,
    get_media_url,
)
from .utils.savers import (
    save_tweets_to_csv,
)
from .secondary_services import (
    define_tweet_type,
)

load_dotenv()

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_key = os.getenv('ACCESS_KEY')
access_secret = os.getenv('ACCESS_SECRET')


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


def get_user_info(screen_name):
    user = api.get_user(screen_name=screen_name)

    query = TwitterUserInfo(
        id = user.id,
        screen_name = user.screen_name,
        name = user.name,
        profile_image_url = user.profile_image_url,
        description = user.description,
        created_at = user.created_at,
        url = user.url,
        location = user.location,
        followers_count = user.followers_count,
        friends_count = user.friends_count,
        favourites_count = user.favourites_count,
        statuses_count = user.statuses_count,
        listed_count = user.listed_count,
        is_protected = user.protected,
        is_verified = user.verified
    )
    query.save()


def get_all_tweets(screen_name):
    all_tweets = []
    tweets = []
    result = []

    try:
        tweets = api.user_timeline(screen_name=screen_name, count=200, tweet_mode='extended')
    except tweepy.errors.Unauthorized:
        return []

    if not tweets:
        return []

    all_tweets.extend(tweets)
    oldest_id = all_tweets[-1].id

    while True:
        tweets = None
        try:
            tweets = api.user_timeline(
                screen_name=screen_name, 
                count=200, 
                max_id=oldest_id-1, 
                tweet_mode='extended'
            )
            
        except tweepy.errors.Unauthorized: pass
        
        if tweets != None:
            if len(tweets) == 0:
                break

            all_tweets.extend(tweets)
            oldest_id = tweets[-1].id

    for tweet in all_tweets:
        tweet_type_info = define_tweet_type(tweet)
        
        coordinates = 'undefined'
        if tweet.coordinates:
            coordinates = tweet.coordinates.get('coordinates')
        
        if not tweet_type_info:
            break

        result.append({
            'id': tweet.id,
            'created_at': str(tweet.created_at),
            'text': tweet.full_text.replace('"', ''),
            'lang': tweet.lang,
            'retweet_count': tweet.retweet_count,
            'favourite_count': tweet.favorite_count,
            'hashtags': get_hashtags(tweet).replace('"', ''),
            'urls': get_urls(tweet).replace('"', ''),
            'user_mentions': get_user_mentions(tweet).replace('"', ''),
            'coordinates': coordinates,
            'source': tweet.source,
            'tweet_type': tweet_type_info.get('tweet_type'),
            'media': get_media_url(tweet).replace('"', ''),
            'original_screen_name': tweet_type_info.get('original_screen_name'),
            'user_id': tweet.user.id
        }) 
    
    return result