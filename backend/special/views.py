import json

import django
import django_celery_beat
from django.db.utils import IntegrityError
from django_celery_beat.models import IntervalSchedule, PeriodicTask, PeriodicTasks
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .celery import *
from .models import Tweets, Users, ActiveCeleryTasks
from .serializers import *
from .services import *
from .tasks import scrape_hashtags, scrape_persons, scrape_limit_hashtags


logger.add("static/logs/views.log", format="{time} {message}", level="INFO", rotation="500 MB", compression="zip", encoding='utf-8')


class V1_DownloadUser(APIView):
    permission_classes = [AllowAny]
    serializer_class = UsersListSerializer

    def get(self, request, screen_name):
        user = v1_get_user(screen_name)

        user_to_save = from_v1_user(user)
        serializer = UsersSerializer(data=user_to_save)
        serializer.is_valid(raise_exception=True)
        
        try:
            serializer.save()
        except IntegrityError:
            logger.warning(f"Этот пользователь ({serializer.data.get('screen_name')}) уже содержится в Базе Данных!")
            serializer.update(Users.objects.get(pk=serializer.data.get('id')), serializer.validated_data)

        return Response(serializer.data)


class V1_DownloadTweetsFromPerson(APIView):
    permission_classes = [AllowAny]
    serializer_class = TweetsSerializer
    downloaded_count = 0
    updated_count = 0

    def get(self, request, screen_name):
        tweets = v1_get_tweets(screen_name)
        if tweets:
            tweets_to_save = list(map(from_v1_tweet, tweets))

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
        else:
            return Response(f'Ничего не загружено! Тут https://twitter.com/{screen_name} есть твиты?')


class V1_DownloadTweetById(APIView):
    permission_classes = [AllowAny]
    serializer_class = TweetsSerializer

    def get(self, request, tweet_id):
        tweet = v1_get_tweet(tweet_id)
        if tweet:
            tweet_to_save = from_v1_tweet(tweet)
            serializer = self.serializer_class(data=tweet_to_save)
            serializer.is_valid(raise_exception=True)

            try:
                serializer.save()
            except IntegrityError:
                logger.warning(f"Этот твит ({serializer.data.get('id')}) уже содержится в Базе Данных!")
                serializer.update(Tweets.objects.get(pk=serializer.data.get('id')), serializer.validated_data)

            return Response(serializer.data)
        else:
            return Response('Нет такого твита...')

    
class V1_DownloadLikesById(APIView):
    permission_classes = [AllowAny]
   
    def get(self, request, screen_name):
        likes = v1_get_likes(screen_name)

        serializer = LikesSerializer(data=likes, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(likes)


class V2_DownloadTweetsByManyHashtags(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        name = request.data.get('name')
        hashtags_values = request.data.get('values')
        mode_flag = int(request.data.get('mode_flag'))
        all_flag = request.data.get('all_flag')

        if name == None:
            return Response('Укажите в POST-запросе поле name с уникальным значением')
        if mode_flag == None:
            return Response('Укажите в POST-запросе поле mode_flag: 1 / 0')
        if all_flag == None and hashtags_values == None and mode_flag == 1:
            return Response('Укажите в POST-запросе поле values: [hashtag_1, ... , hashtag_n] или all_flag: true / false')

        if mode_flag == 1:
            if all_flag:
                hashtags_values = Hashtags.objects.all().values('value')
                hashtags_values = [hashtag.get('value') for hashtag in hashtags_values]

            logger.debug(f"all_flag values: {hashtags_values}")
            delayed_task = scrape_hashtags.delay(hashtags_values, name)
            celery_task = ActiveCeleryTasks(name=name, task_id=delayed_task.id, entities=hashtags_values)
            celery_task.save()
            settings.REDIS_INSTANCE.set(name, 1)

            return Response(f'Started celery task with id {delayed_task.id}')

        elif mode_flag == 0:
            active_celery_task = ActiveCeleryTasks.objects.get(pk=name)
            scrape_hashtags.AsyncResult(active_celery_task.task_id).revoke()
            active_celery_task.delete()
            settings.REDIS_INSTANCE.set(name, 0)
            logger.info(f"Task '{name}' was stopped")

            return Response(f"Stopped celery task with name '{name}'")
        
        else:
            return Response('Укажите в POST-запросе поле mode_flag: 1 / 0')


class V2_DownloadTweetsByLimit(APIView):
    permission_classes = [AllowAny]

    def get(self, request, max_count):
        hashtags_values = Hashtags.objects.all().values('value')
        hashtags_values = [hashtag.get('value') for hashtag in hashtags_values] 

        delayed_task = scrape_limit_hashtags.delay(hashtags_values, max_count)
            
        return Response(f"Started limited ({max_count}) scraping tweets by all hashtags")


class V2_DownloadUser(APIView): 
    permission_classes = [AllowAny]
    serializer_class = UsersSerializer
    
    def get(self, request, screen_name):
        user = v2_get_user(screen_name)
        print(user)
        user_to_save = from_v2_user(user)
        serializer = UsersSerializer(data=user_to_save)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
            logger.info(f"Этот пользователь ({serializer.data.get('screen_name')}) только что был добавлен в Базу Данных!")
        except IntegrityError:
            logger.warning(f"Этот пользователь ({serializer.data.get('screen_name')}) уже содержится в Базе Данных!")
            serializer.update(Users.objects.get(pk=serializer.data.get('id')), serializer.validated_data)

        return Response(serializer.data)


class V2_DownloadCommentsByScreenName(APIView):
    permission_classes = [AllowAny]
    serializer_class = RepliesListSerializer

    def get(self, request, screen_name, max_count):
        v2_download_comments(screen_name, max_count)

        comments = Replies.objects.filter(author_screen_name=screen_name)
        serializer = self.serializer_class(instance=comments, many=True)

        return Response(serializer.data)


class GetHashtagsFromFile(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        hashtags = download_hashtags_from_file()
        return Response(hashtags)


class MonitoringHashtags(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        name = request.data.get('name')
        hashtags_values = request.data.get('values')
        mode_flag = int(request.data.get('mode_flag'))
        all_flag = request.data.get('all_flag')
        interval = request.data.get('interval')

        if name == None:
            return Response('Укажите в POST-запросе поле name с уникальным значением')
        if mode_flag == None:
            return Response('Укажите в POST-запросе поле mode_flag: 1 / 0')
        if interval == None:
            return Response('Укажите в POST-запросе поле interval (в часах): 1..n')
        if all_flag == None and hashtags_values == None and mode_flag == 1:
            return Response('Укажите в POST-запросе поле values: [hashtag_1, ... , hashtag_n] или all_flag: true / false')

        try:
            schedule = IntervalSchedule.objects.create(every=interval, period=IntervalSchedule.HOURS)
        except django_celery_beat.models.IntervalSchedule.MultipleObjectsReturned:
            schedule = IntervalSchedule.objects.filter(every=interval, period=IntervalSchedule.HOURS).delete()
            schedule = IntervalSchedule.objects.create(every=interval, period=IntervalSchedule.HOURS)

        if all_flag:
            hashtags_values = Hashtags.objects.all().values('value')
            hashtags_values = [hashtag.get('value') for hashtag in hashtags_values]

        if mode_flag:
            settings.REDIS_INSTANCE.set(name, 1)
            try:
                task = PeriodicTask.objects.create(
                    interval=schedule, 
                    name='scrape_hashtags', 
                    task='special.tasks.scrape_hashtags', 
                    args=json.dumps([hashtags_values, name]))

            except django.core.exceptions.ValidationError:
                task = PeriodicTask.objects.filter(
                    name='scrape_hashtags', 
                    task='special.tasks.scrape_hashtags').delete()
                    
                task = PeriodicTask.objects.create(
                    interval=schedule, 
                    name='scrape_hashtags', 
                    task='special.tasks.scrape_hashtags', 
                    args=json.dumps([hashtags_values, name]))

            task.save()
            PeriodicTask.objects.update(last_run_at=None)
            PeriodicTasks.changed(task)

            return Response(str(task))
        else:
            task = PeriodicTask.objects.filter(name='scrape_hashtags', task='special.tasks.scrape_hashtags').delete()
            scrape_hashtags.delay(hashtags_values, name)

            active_celery_task = ActiveCeleryTasks.objects.get(pk=name)
            scrape_hashtags.AsyncResult(active_celery_task.task_id).revoke()
            active_celery_task.delete()
            settings.REDIS_INSTANCE.set(name, 0)
            logger.info(f"Task '{name}' was stopped")

            return Response(f"Stopped celery task with name '{name}' and periodic {str(task)}")


class MonitoringUsers(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        person_screen_names = request.data.get('values')
        mode_flag = request.data.get('mode_flag')
        all_flag = request.data.get('all_flag')
        interval = request.data.get('interval')

        if mode_flag == None:
            return Response('Укажите в POST-запросе поле mode_flag: 1 / 0')
        if interval == None:
            return Response('Укажите в POST-запросе поле interval (в часах, целое число): 1..n')
        if all_flag == None and person_screen_names == None and mode_flag == 1:
            return Response('Укажите в POST-запросе поле values: [screen_name_1, ... , screen_name_n] или all_flag: true / false')

        if all_flag:
            persons_screen_names = Users.objects.all().values('screen_name')
            persons_screen_names = [person_screen_name.get('screen_name') for person_screen_name in persons_screen_names] 

        # for person_screen_name in persons_screen_names:
        #     settings.REDIS_INSTANCE.set(person_screen_name, mode_flag)

        try:
            schedule = IntervalSchedule.objects.create(every=interval, period=IntervalSchedule.HOURS)
        except django_celery_beat.models.IntervalSchedule.MultipleObjectsReturned:
            schedule = IntervalSchedule.objects.filter(every=interval, period=IntervalSchedule.HOURS).delete()
            schedule = IntervalSchedule.objects.create(every=interval, period=IntervalSchedule.HOURS)

        if mode_flag:
            try:
                task = PeriodicTask.objects.create(
                    interval=schedule, 
                    name='scrape_persons', 
                    task='special.tasks.scrape_persons', 
                    args=json.dumps([person_screen_names]))

            except django.core.exceptions.ValidationError:
                task = PeriodicTask.objects.filter(
                    name='scrape_persons', 
                    task='special.tasks.scrape_persons').delete()
                    
                task = PeriodicTask.objects.create(
                    interval=schedule, 
                    name='scrape_persons', 
                    task='special.tasks.scrape_persons', 
                    args=json.dumps([person_screen_names]))

            task.save()
            PeriodicTask.objects.update(last_run_at=None)
            PeriodicTasks.changed(task)

            return Response(str(task))
        else:
            task = PeriodicTask.objects.filter(name='scrape_persons', task='special.tasks.scrape_persons').delete()
            scrape_persons.delay(person_screen_names)

            return Response(str(task)) 


class DatabaseToCSV(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        df = pd.DataFrame(list(Users.objects.all().values()))
        df.to_csv('static/Users.csv', index=0)
        
        df = pd.DataFrame(list(Tweets.objects.all().values()))
        df.to_csv('static/Tweets.csv', index=0)

        df = pd.DataFrame(list(Likes.objects.all().values()))
        df.to_csv('static/Likes.csv', index=0)

        df = pd.DataFrame(list(Replies.objects.all().values()))
        df.to_csv('static/Replies.csv', index=0)

        return Response('Файлы сохранены!') 


class TweetsByHashtagToCSV(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        hashtags_length = {}

        df = pd.DataFrame(list(Tweets.objects.all().values()))

        hashtags_values = Hashtags.objects.all().values('value')
        hashtags_values = [hashtag.get('value') for hashtag in hashtags_values] 

        new_df = df.loc[df.hashtags.notnull()]

        for hashtag in hashtags_values: 
            hashtag_df = new_df.loc[new_df.hashtags.map(lambda x: hashtag in x)]
            hashtag_df.to_csv(f"static/{hashtag}_tweets.csv", index=0)
            hashtags_length[hashtag] = len(hashtag_df)

        return Response(hashtags_length) 