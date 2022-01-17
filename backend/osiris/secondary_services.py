import os
from collections import Counter

import tweepy
from dotenv import load_dotenv

from .utils.getters import (
    get_domain,
)
from .utils.formatters import (
    get_tweet_weekday,
    get_tweet_time_of_weekdays,
    get_tweet_dates,
)


load_dotenv()

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_key = os.getenv('ACCESS_KEY')
access_secret = os.getenv('ACCESS_SECRET')


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


def get_domain_count(urls):
    """Getting urls from tweet"""
    if len(urls) == 0:
        return 'Not found'
    else:
        domains = []
        for url in urls:
            domains.append(get_domain(url))
            
        urls_counter = Counter(domains)
        
        return {'urls': [{url: count} for url, count in urls_counter.items()]}
    

def get_tweet_retweet_screen_name(retweet_screen_names):
    """Getting retweet's screen name from tweet"""

    retweet_screen_names_counter = Counter(retweet_screen_names)

    if len(retweet_screen_names_counter) != 0:
        return {'retweet_screen_names': [{screen_name: count} for screen_name, count in retweet_screen_names_counter.items()]} 
    else:
        return 'Not found'
    

def get_tweet_quote_screen_name(quote_screen_names):
    """Getting quote's screen name"""

    quote_screen_names_counter = Counter(quote_screen_names)

    if len(quote_screen_names_counter) != 0:
        return {'quote_screen_names': [{screen_name: count} for screen_name, count in quote_screen_names_counter.items()]}
    else:
        return 'Not found'
    

def get_source_count(sources):
    """Getting tweet's source"""
    
    sources = Counter(sources)
    
    if len(sources) == 0:
        return 'Not found'
    else:
        return {'sources': [{source: count} for source,count in sources.items()]}
    

def get_lang_count(langs):
    """getting tweet's langs"""
    
    langs = Counter(langs)

    if len(langs) == 0:
        return 'Not found'
    else:
        return {'langs': [{lang: count} for lang, count in langs.items()]}
    

def calculate_user_mentions(user_mentions):
    """Getting user mentions of tweets"""

    user_mentions = Counter(user_mentions)
    if len(user_mentions) == 0:
        return 'Not found'
    else:
        return {'user_mentions': [{mention: count} for mention, count in user_mentions.items()]}
           

def calculate_hashtags(hashtags):
    """Getting tweet's hashtags"""
    
    hashtags = Counter(hashtags)
        
    if len(hashtags) == 0:
        return 'Not found'
    else:
        return {'hashtags': [{hashtag: count} for hashtag, count in hashtags.items()]}


def calculate_network_activity(datetimes):
    """Calculate network activity of user by tweets time data"""
    
    weekdays_time = get_tweet_time_of_weekdays(datetimes) 
    sorted_weekdays_time = [weekdays_time.get('Sunday'), weekdays_time.get('Monday'), weekdays_time.get('Tuesday'), 
                            weekdays_time.get('Wednesday'), weekdays_time.get('Thursday'), 
                            weekdays_time.get('Friday'), weekdays_time.get('Saturday')] 

    if len(weekdays_time) == 0:
        return 'Not found'
    else:
        return {'weekdays_time': sorted_weekdays_time}
    

def calculate_day_tweets(datetimes):
    """Calculate count of tweeys in different days"""
    
    dates = get_tweet_dates(datetimes)

    if len(dates) == 0:
        return 'Not found'
    else:
        return [{day: count} for day, count in dates.items()]


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