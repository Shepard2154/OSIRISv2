from datetime import datetime

from channels.layers import get_channel_layer

from multiprocessing import AuthenticationError
import statistics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView, 
)

from django.conf import settings
from django.db.utils import IntegrityError

from .v2_services import *
from .v1_services import *
from .statistics import calculate_tweets_type
from .serializers import *
from .models import TwitterUser, TwitterTweet
from .cli import download_mytweets, download_username

import redis


logger.add("logs/views.log", format="{time} {message}", level="DEBUG", rotation="500 MB", compression="zip", encoding='utf-8')


redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

class DownloadPerson(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def get(self, request, screen_name):
        user = get_user_info(screen_name)
        print(user)
        # desired_user = UserSerializer.objects.get(screen_name=screen_name).__dict__
        # serializer = self.serializer_class(data=desired_user)
        # serializer.is_valid(raise_exception=True)
        
        # return Response(serializer.data)
        return Response(user)


class DownloadTweets(APIView):
    permission_classes = [AllowAny]
    serializer_class = TweetListSerializer

    def get(self, request, screen_name):
        tweets = download_all_tweets(screen_name)
        save_tweets(tweets)

        user_id = TwitterUser.objects.get(screen_name=screen_name).id
        tweets = TwitterTweet.objects.all().filter(user_id=user_id)
        serializer = self.serializer_class(instance=tweets, many=True)
        
        return Response(serializer.data)


class V1_DownloadTweet(APIView):
    permission_classes = [AllowAny]

    def get(self, request, tweet_id):
        tweet = v1_get_tweet_by_id(tweet_id)._json
        
        return Response(tweet)


# class V2_DownloadTweetsByHashtag(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request, hashtag_value):
#         tweet = download_tweets(hashtag_value)
        
#         return Response(tweet[0])


class CalculateTweetsStatistics(APIView):
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def get(self, request, screen_name):
        statistics = get_tweets_statistics(screen_name)
        print(statistics)
        
        return Response('Ok')
        # quotes = models.JSONField(null=True)
        # retweets = models.JSONField(null=True)

        # serializer = self.serializer_class(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()



# class V2_DownloadHashtags(APIView):
#     permission_classes = [AllowAny]
#     serializer = TweetSerializer()

#     def get(self, request, hashtag_value, power):
#         for tweet in download_mytweets(hashtag_value):
#             print(tweet['url'])
#             self.serializer.from_v2_tweet(tweet=tweet)
#             self.serializer.is_valid(raise_exception=True)
#             self.serializer.save()
        
#         return Response('Ok')

        
class V2_DownloadHashtags(APIView):
    permission_classes = [AllowAny]
    serializer_class = TweetSerializer

    def get(self, request, hashtag_value, power):
        redis_instance.set(hashtag_value, power)
        for tweet in download_mytweets(hashtag_value):
            if int(redis_instance.get(hashtag_value)):
                tweet_to_save = from_v2_tweet(tweet)
                serializer = self.serializer_class(data=tweet_to_save)
                serializer.is_valid(raise_exception=True)
                try:
                    serializer.save()
                except IntegrityError:
                    logger.warning(f"Этот твит ({serializer.data.get('id')}) уже содержится в Базе Данных! Скачивание приостановлено.")
                    serializer.update(TwitterTweet.objects.get(pk=serializer.data.get('id')), serializer.validated_data)
            else:
                return Response(f"Сбор по {'#' + hashtag_value} прекращен!")


class V2_DownloadPerson(APIView): 
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    
    def get(self, request, username, power):
        person = download_username(username)
        person_to_save = from_v2_user(person)
        print(person_to_save)

        serializer = self.serializer_class(data=person_to_save)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except IntegrityError:
            logger.warning(f"Этот пользователь ({serializer.data.get('screen_name')}) уже содержится в Базе Данных!")
            serializer.update(TwitterTweet.objects.get(pk=serializer.data.get('id')), serializer.validated_data)

        return Response(serializer.data)