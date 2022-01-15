import tweepy
import csv
import calendar

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


consumer_key = 'u4SD5KlVGm59ftBTb69glEtp1'
consumer_secret = 'PCSFhTShUoKzASdExZh5pz54nP1v4uo0KheBotPpZUUoQ3r1sV'
access_key = '2308267840-G9kog927ZlVhGvoUsXbIt16ZQLk0eUkeuteieA6'
access_secret = '6ZW7GNAZTG6tW4YXYShawMgGbv5ri4kfZvgDF1UAbSb4a'


def get_all_tweets(screen_name):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    alltweets = []  
    
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    alltweets.extend(new_tweets)

    oldest = alltweets[-1].id - 1
    
    while len(new_tweets) > 0:
        print(f"getting tweets before {oldest}")
        
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        alltweets.extend(new_tweets)
        
        oldest = alltweets[-1].id - 1
        
        print(f"...{len(alltweets)} tweets downloaded so far")
    

    for item in alltweets[0].user._json:
        print(item, ' : ', alltweets[0].user._json[item])
            
    tweets = [{'tweet_id': tweet.id_str, 'tweet_created_at': tweet.created_at, 'tweet_text': tweet.text} for tweet in alltweets]

    return tweets


def save_tweets_csv(screen_name, tweets):
    with open(f'new_{screen_name}_tweets.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(tweets)


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


def au():
    token = Token.objects.create(user='@wh1Co4nkIcsfUnR')
    print(token.key)

    for user in User.objects.all():
        print(user)