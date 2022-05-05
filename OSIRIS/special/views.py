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
from .models import Tweets, Users
from .serializers import *
from .services import *
from .tasks import scrape_hashtags, scrape_persons


logger.add("static/logs/views.log", format="{time} {message}", level="INFO", rotation="500 MB", compression="zip", encoding='utf-8')


class V1_DownloadUser(APIView):
    permission_classes = [AllowAny]
    serializer_class = UsersListSerializer

    def get(self, request, screen_name):
        v1_download_user(screen_name)

        user = Users.objects.filter(screen_name=screen_name)
        serializer = self.serializer_class(instance=user, many=True)

        return Response(serializer.data)


class V1_GetTweetsFromPerson(APIView):
    permission_classes = [AllowAny]
    serializer_class = TweetsSerializer
    downloaded_count = 0
    updated_count = 0

    def get(self, request, screen_name):
        tweets_to_save = list(map(from_v1_tweet, v1_get_tweets(screen_name)))

        for tweet in tweets_to_save:
            serializer = self.serializer_class(data=tweet)
            serializer.is_valid(raise_exception=True)
            try:
                serializer.save()
                self.downloaded_count += 1
            except IntegrityError:
                logger.warning(f"Этот твит ({serializer.data.get('id')}) уже содержится в Базе Данных!")
                serializer.update(Tweets.objects.get(pk=serializer.data.get('id')), serializer.validated_data)
                self.updated_count += 1

        return Response(f"{self.downloaded_count} новых твитов {screen_name} добавлено в БД! {self.updated_count} обновлено!")


class V1_DownloadTweetById(APIView):
    permission_classes = [AllowAny]
    serializer_class = TweetsSerializer

    def get(self, request, tweet_id):
        tweet = v1_get_tweet(tweet_id)._json
        
        tweet_to_save = from_v1_tweet(tweet)
        serializer = self.serializer_class(data=tweet_to_save)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except IntegrityError:
            logger.warning(f"Этот твит ({serializer.data.get('id')}) уже содержится в Базе Данных!")
            serializer.update(Tweets.objects.get(pk=serializer.data.get('id')), serializer.validated_data)

        return Response(tweet)

        
class V2_DownloadTweetsByHashtags(APIView):
    permission_classes = [AllowAny]
    serializer_class = TweetsSerializer
    downloaded_count = 0

    def get(self, request, hashtag_value, power):
        settings.REDIS_INSTANCE.set(hashtag_value, power)
        for tweet in v2_download_tweets_by_hashtag(hashtag_value):
            if int(settings.REDIS_INSTANCE.get(hashtag_value)):
                tweet_to_save = from_v2_tweet(tweet)
                serializer = self.serializer_class(data=tweet_to_save)
                serializer.is_valid(raise_exception=True)
                try:
                    serializer.save()
                    self.downloaded_count += 1
                except IntegrityError:
                    logger.warning(f"Этот твит ({serializer.data.get('id')}) уже содержится в Базе Данных!")
                    serializer.update(Tweets.objects.get(pk=serializer.data.get('id')), serializer.validated_data)
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


class V2_DownloadUser(APIView): 
    permission_classes = [AllowAny]
    serializer_class = UsersSerializer
    
    def get(self, request, screen_name):
        v2_download_user(screen_name)
        
        settings.REDIS_INSTANCE.set(screen_name, 1)

        user = Users.objects.filter(screen_name=screen_name)
        serializer = self.serializer_class(instance=user, many=True)

        return Response(serializer.data)


class GetHashtagsFromFile(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        hashtags = get_hashtags_from_file()
        return Response(hashtags)


class MonitoringHashtags(APIView):
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
                        task='special.tasks.scrape_hashtags', 
                        args=json.dumps([hashtags_values, all_flag, mode_flag]))

                except django.core.exceptions.ValidationError:
                    task = PeriodicTask.objects.filter(
                        name='scrape_hashtags', 
                        task='special.tasks.scrape_hashtags').delete()
                        
                    task = PeriodicTask.objects.create(
                        interval=schedule, 
                        name='scrape_hashtags', 
                        task='special.tasks.scrape_hashtags', 
                        args=json.dumps([hashtags_values, all_flag, mode_flag]))

                task.save()
                PeriodicTask.objects.update(last_run_at=None)
                PeriodicTasks.changed(task)

                return Response(str(task))
            else:
                task = PeriodicTask.objects.filter(name='scrape_hashtags', task='special.tasks.scrape_hashtags').delete()
                scrape_hashtags.delay(hashtags_values, all_flag, mode_flag)

                return Response(str(task))


class MonitoringUsers(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        person_screen_names = request.data.get('values')
        mode_flag = int(request.data.get('mode_flag'))
        all_flag = request.data.get('all_flag')
        interval = request.data.get('interval')

        if mode_flag == None:
            return Response('Укажите в POST-запросе поле mode_flag: 1 / 0')
        if interval == None:
            return Response('Укажите в POST-запросе поле interval (в часах): 1..n')
        if person_screen_names or all_flag:
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
                        name='scrape_persons', 
                        task='special.tasks.scrape_persons', 
                        args=json.dumps([person_screen_names, all_flag, mode_flag]))

                except django.core.exceptions.ValidationError:
                    task = PeriodicTask.objects.filter(
                        name='scrape_persons', 
                        task='special.tasks.scrape_persons').delete()
                        
                    task = PeriodicTask.objects.create(
                        interval=schedule, 
                        name='scrape_persons', 
                        task='special.tasks.scrape_persons', 
                        args=json.dumps([person_screen_names, all_flag, mode_flag]))

                task.save()
                PeriodicTask.objects.update(last_run_at=None)
                PeriodicTasks.changed(task)

                return Response(str(task))
            else:
                task = PeriodicTask.objects.filter(name='scrape_persons', task='special.tasks.scrape_persons').delete()
                scrape_persons.delay(person_screen_names, all_flag, mode_flag)

                return Response(str(task)) 


class V1_DownloadLikesById(APIView):
    permission_classes = [AllowAny]
   
    def get(self, request, screen_name):
        data = v1_get_likes(screen_name)
        serializer = LikesSerializer(data=data, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data)


class V2_DownloadCommentsByScreenName(APIView):
    permission_classes = [AllowAny]
    serializer_class = RepliesListSerializer

    def get(self, request, screen_name, max_count):
        v2_get_comments(screen_name, max_count)
        comments = Replies.objects.filter(author_screen_name=screen_name)
        serializer = self.serializer_class(instance=comments, many=True)
        return Response(serializer.data)