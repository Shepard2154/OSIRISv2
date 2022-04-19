import os
from datetime import datetime

import tweepy
from dateutil.parser import parse
from dotenv import load_dotenv
from loguru import logger

import twitter

from .models import TwitterTweet, TwitterUser
from .statistics import (calculate_day_tweets, calculate_hashtags,
                         calculate_network_activity, calculate_tweets_type,
                         calculate_user_mentions, get_domain_count,
                         get_lang_count, get_source_count, get_tweet_dates,
                         get_tweet_quote_screen_name,
                         get_tweet_retweet_screen_name,
                         get_tweet_time_of_weekdays, get_tweet_weekday)
from .utils.getters import (get_hashtags, get_media_url, get_urls,
                            get_user_mentions)

logger.add("logs/twitterAPIv1_services.log", format="{time} {message}", level="DEBUG", rotation="500 MB", compression="zip", encoding='utf-8')

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
    user = api.get_user(screen_name=screen_name)._json
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


# def save_tweets(tweets):
#     logger.debug(f"downloaded {len(tweets)}")
#     for tweet in tweets:
#         coordinates = 'undefined'
#         if tweet.coordinates:
#             coordinates = tweet.coordinates.get('coordinates')

#         tweet_type_info = define_tweet_type(tweet)
#         if not tweet_type_info:
#             break

#         tweet = TwitterTweet(
#             id = tweet.id,
#             created_at = tweet.created_at,
#             text = tweet.full_text.replace('"', ''),
#             lang = tweet.lang,
#             retweet_count = tweet.retweet_count,
#             favorite_count = tweet.favorite_count,
#             hashtags = get_hashtags(tweet).replace('"', ''),
#             urls = get_urls(tweet).replace('"', ''),
#             user_mentions = get_user_mentions(tweet).replace('"', ''),
#             coordinates = coordinates,
#             source = tweet.source,
#             tweet_type = tweet_type_info.get('tweet_type'),
#             media = get_media_url(tweet).replace('"', ''),
#             original_screen_name = tweet_type_info.get('original_screen_name'),
#             user_id = TwitterUser.objects.get(pk=tweet.user.id)
#         )

#         try:
#             TwitterTweet.objects.get(pk=tweet.id)  
#         except twitter.models.TwitterTweet.DoesNotExist:
#             tweet.save()


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


