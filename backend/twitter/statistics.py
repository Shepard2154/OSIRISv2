import calendar
from collections import Counter
from datetime import datetime

from .models import TwitterTweet
from .serializers import TweetListSerializer
from .utils.formatters import (get_tweet_dates, get_tweet_time_of_weekdays,
                               get_tweet_weekday)
from .utils.getters import get_domain


def get_domain_count(urls):
    if len(urls) == 0:
        return 'Not found'
    else:
        domains = []
        for url in urls:
            domains.append(get_domain(url))
            
        urls_counter = Counter(domains)
        
        return {'urls': [{url: count} for url, count in urls_counter.items()]}
    

def get_tweet_retweet_screen_name(retweet_screen_names):
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
    weekdays_time = get_tweet_time_of_weekdays(datetimes) 
    sorted_weekdays_time = [weekdays_time.get('Sunday'), weekdays_time.get('Monday'), weekdays_time.get('Tuesday'), 
                            weekdays_time.get('Wednesday'), weekdays_time.get('Thursday'), 
                            weekdays_time.get('Friday'), weekdays_time.get('Saturday')] 

    if len(weekdays_time) == 0:
        return 'Not found'
    else:
        return {'weekdays_time': sorted_weekdays_time}
    

def calculate_day_tweets(datetimes):
    """Calculate count of tweets in different days"""
    
    dates = get_tweet_dates(datetimes)

    if len(dates) == 0:
        return 'Not found'
    else:
        return [{day: count} for day, count in dates.items()]


# def calculate_tweets_type(user_id):
#     tweets = TwitterTweet.objects.all().filter(user_id=user_id)
#     serializer = TweetListSerializer(instance=tweets, many=True)
#     print(serializer.data)

#     counter = Counter(tweets)
#     return counter.items()

def calculate_tweets_type(tweet_types):
    counter = Counter(tweet_types)
    return counter.items()


def get_tweet_time_of_weekdays(data):
    weekdays = {
        'Sunday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0], 
        'Monday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0], 
        'Tuesday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0], 
        'Wednesday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0], 
        'Thursday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0], 
        'Friday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0], 
        'Saturday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0]
        }
    
    for item in data:
        if weekdays.get(str(calendar.day_name[item.weekday()])):
            time = str(item.time())[0:2]
            weekdays[str(calendar.day_name[item.weekday()])][int(time)] += 1
        else:
            weekdays[str(calendar.day_name[item.weekday()])] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0]
    return weekdays


def get_tweet_weekday(data):
    weekdays = {'Sunday': 0, 'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0}

    for item in data:
        if weekdays.get(str(calendar.day_name[item.weekday()])): 
            weekdays[str(calendar.day_name[item.weekday()])] += 1
        else:
            weekdays[str(calendar.day_name[item.weekday()])] = 1
    return weekdays


def get_tweet_dates(data):
    dates = {}
    for item in data:
        if dates.get(str(item.date())): 
            dates[str(item.date())] += 1
        else:
            dates[str(item.date())] = 1
    return dates