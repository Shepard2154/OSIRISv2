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

class V1_DownloadPerson(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def get(self, request, screen_name):
        person = get_user_info(screen_name)
        person_to_save = from_v1_user(person)

        serializer = self.serializer_class(data=person_to_save)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except IntegrityError:
            logger.warning(f"Этот пользователь ({serializer.data.get('screen_name')}) уже содержится в Базе Данных!")
            serializer.update(TwitterUser.objects.get(pk=serializer.data.get('id')), serializer.validated_data)

        return Response(serializer.data)


class V1_DownloadTweetsFromPerson(APIView):
    permission_classes = [AllowAny]
    serializer_class = TweetSerializer

    def get(self, request, screen_name):
        tweets = download_all_tweets(screen_name)
        tweets_to_save = list(map(from_v1_tweet, tweets))
        serializer = self.serializer_class(data=tweets_to_save, many=True)
        serializer.is_valid()
        serializer.save()

        return Response(serializer.data)


class V1_GetTweetById(APIView):
    permission_classes = [AllowAny]

    def get(self, request, tweet_id):
        tweet = v1_get_tweet_by_id(tweet_id)._json
        
        return Response(tweet)

        
class V2_DownloadTweetsByHashtags(APIView):
    permission_classes = [AllowAny]
    serializer_class = TweetSerializer
    downloaded_count = 0

    def get(self, request, hashtag_value, power):
        redis_instance.set(hashtag_value, power)
        for tweet in download_mytweets(hashtag_value):
            if int(redis_instance.get(hashtag_value)):
                tweet_to_save = from_v2_tweet(tweet)
                serializer = self.serializer_class(data=tweet_to_save)
                serializer.is_valid(raise_exception=True)
                try:
                    serializer.save()
                    self.downloaded_count += 1
                except IntegrityError:
                    logger.warning(f"Этот твит ({serializer.data.get('id')}) уже содержится в Базе Данных! Скачивание приостановлено.")
                    serializer.update(TwitterTweet.objects.get(pk=serializer.data.get('id')), serializer.validated_data)
            else:
                return Response(f"Сбор по {'#' + hashtag_value} прекращен!")
        return Response(f"Сбор по {'#' + hashtag_value} успешно завершен! Собрано {self.downloaded_count} твитов в БД")


class V2_DownloadPerson(APIView): 
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    
    def get(self, request, username):
        person = download_username(username)
        person_to_save = from_v2_user(person)
        print(person_to_save)

        serializer = self.serializer_class(data=person_to_save)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except IntegrityError:
            logger.warning(f"Этот пользователь ({serializer.data.get('screen_name')}) уже содержится в Базе Данных!")
            serializer.update(TwitterUser.objects.get(pk=serializer.data.get('id')), serializer.validated_data)

        return Response(serializer.data)


class CalculateUserStatistics(APIView):
    permission_classes = [AllowAny]

    def get(self, request, screen_name):
        # statistics = get_tweets_statistics(screen_name)
        # print(statistics)
        # quotes = models.JSONField(null=True)
        # retweets = models.JSONField(null=True)

        # serializer = self.serializer_class(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        return Response('Does not work :(')
        