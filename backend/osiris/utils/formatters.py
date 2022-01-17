import calendar
from datetime import datetime


def get_tweet_dates(tweets):
    dates = {}
    for tweet in tweets:
        if dates.get(str(tweet['tweet_created_at'].date())): 
            dates[str(tweet['tweet_created_at'].date())] += 1
        else:
            dates[str(tweet['tweet_created_at'].date())] = 1
    return dates


def get_tweet_time(tweets):
    time = {}
    for tweet in tweets:
        if time.get(str(tweet['tweet_created_at'].time())[0:2]): 
            time[str(tweet['tweet_created_at'].time())[0:2]] += 1
        else:
            time[str(tweet['tweet_created_at'].time())[0:2]] = 1
    return time


def get_tweet_weekday(tweets):
    weekdays = {}
    for tweet in tweets:
        if weekdays.get(calendar.day_name[tweet['tweet_created_at'].weekday()]): 
            weekdays[calendar.day_name[tweet['tweet_created_at'].weekday()]] += 1
        else:
            weekdays[calendar.day_name[tweet['tweet_created_at'].weekday()]] = 1
    return weekdays


def get_tweet_time_of_weekdays(data):
    """To receive hours of tweet of the days of a week"""
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
        if weekdays.get(str(calendar.day_name[datetime.strptime(item, "%Y-%m-%d %H:%M:%S%z").weekday()])):
            time = str(datetime.strptime(item, "%Y-%m-%d %H:%M:%S%z").time())[0:2]
            weekdays[str(calendar.day_name[datetime.strptime(item, "%Y-%m-%d %H:%M:%S%z").weekday()])][int(time)] += 1
        else:
            weekdays[str(calendar.day_name[datetime.strptime(item, "%Y-%m-%d %H:%M:%S%z").weekday()])] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0]
    return weekdays