import json

import django
import django_celery_beat
from django.db.utils import IntegrityError
from django.conf import settings
from django_celery_beat.models import IntervalSchedule, PeriodicTask, PeriodicTasks
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .celery import *
from .models import TwitterTweet, TwitterUser
from .serializers import *
from .services import *
from .tasks import example, scrape_hashtags


logger.add("logs/views.log", format="{time} {message}", level="DEBUG", rotation="500 MB", compression="zip", encoding='utf-8')

# class Webdriver_DownloadTweetsByHashtags(APIView):
#     permission_classes = [AllowAny]
    
#     def get(self, request, hashtag_value):
#         return Response('Does not work :(')


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
        settings.REDIS_INSTANCE.set(hashtag_value, power)
        for tweet in download_tweets_by_hashtag(hashtag_value):
            if int(settings.REDIS_INSTANCE.get(hashtag_value)):
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


class V2_DownloadTweetsByManyHashtags(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        hashtags_values = request.data.get('values')
        mode_flag = int(request.data.get('mode_flag'))
        all_flag = request.data.get('all_flag')
        
        if mode_flag == None:
            return Response('Укажите в POST-запросе поле mode_flag: 1 / 0')
        if hashtags_values or all_flag:
            scrape_hashtags.delay(hashtags_values, all_flag, mode_flag)
            return Response('ok')
        else:
            return Response('Укажите в POST-запросе поле values: [hashtag_1, ... , hashtag_n] или all_flag: true / false')


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


class GetHashtagsFromFile(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        hashtags = get_hashtags_from_file()
        return Response(hashtags)


class Monitoring(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        hashtags_values = request.data.get('values')
        mode_flag = int(request.data.get('mode_flag'))
        all_flag = request.data.get('all_flag')
        interval = request.data.get('interval')

        if mode_flag == None:
            return Response('Укажите в POST-запросе поле mode_flag: 1 / 0')
        if interval == None:
            return Response('Укажите в POST-запросе поле interval (в часах): 1..n')
        if hashtags_values or all_flag:
            try:
                # Для удобного тестирования оставил интервал в секундах
                schedule = IntervalSchedule.objects.create(every=interval, period=IntervalSchedule.SECONDS)
            except django_celery_beat.models.IntervalSchedule.MultipleObjectsReturned:
                schedule = IntervalSchedule.objects.filter(every=interval, period=IntervalSchedule.SECONDS).delete()
                schedule = IntervalSchedule.objects.create(every=interval, period=IntervalSchedule.SECONDS)

            if mode_flag:
                try:
                    task = PeriodicTask.objects.create(
                        interval=schedule, 
                        name='scrape_hashtags', 
                        task='twitter.tasks.scrape_hashtags', 
                        args=json.dumps([hashtags_values, all_flag, mode_flag]))

                except django.core.exceptions.ValidationError:
                    task = PeriodicTask.objects.filter(
                        name='scrape_hashtags', 
                        task='twitter.tasks.scrape_hashtags').delete()
                        
                    task = PeriodicTask.objects.create(
                        interval=schedule, 
                        name='scrape_hashtags', 
                        task='twitter.tasks.scrape_hashtags', 
                        args=json.dumps([hashtags_values, all_flag, mode_flag]))

                task.save()
                PeriodicTask.objects.update(last_run_at=None)
                PeriodicTasks.changed(task)

                return Response(str(task))
            else:
                task = PeriodicTask.objects.filter(name='scrape_hashtags', task='twitter.tasks.scrape_hashtags').delete()
                scrape_hashtags.delay(hashtags_values, all_flag, mode_flag)

                return Response(str(task))


# class CalculateUserStatistics(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request, screen_name):
#         # statistics = get_tweets_statistics(screen_name)
#         # print(statistics)
#         # quotes = models.JSONField(null=True)
#         # retweets = models.JSONField(null=True)

#         # serializer = self.serializer_class(data=request.data)
#         # serializer.is_valid(raise_exception=True)
#         # serializer.save()
#         return Response('Does not work :(')