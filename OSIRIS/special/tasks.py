import multiprocessing as mp

from celery import shared_task
from django.conf import settings
from loguru import logger

from .models import Hashtags, Profiles, Users
from .services import *


logger.add("static/logs/special_tasks.log", format="{time} {message}", level="DEBUG", rotation="500 MB", compression="zip", encoding='utf-8')


@shared_task(bind=True, time_limit=31536000)
def scrape_hashtags(self, hashtags_values, all_flag, mode_flag):
    if all_flag:
        hashtags_values = Hashtags.objects.all().values('value')
        hashtags_values = [hashtag.get('value') for hashtag in hashtags_values] 

    for hashtag_value in hashtags_values:
        settings.REDIS_INSTANCE.set(hashtag_value, mode_flag)

    if mode_flag:
        with mp.Pool(processes=3) as pool:
            pool.map(v2_download_tweets_by_hashtag, hashtags_values)

        # pool.map(v2_download_tweets_by_hashtag, hashtags_values)

        # for hashtag_value in hashtags_values:
        #     v2_download_tweets_by_hashtag(hashtag_value)


@shared_task(bind=True, time_limit=31536000)
def scrape_persons(self, persons_screen_names, all_flag, mode_flag):
    if all_flag:
        persons_screen_names = Users.objects.all().values('screen_name')
        persons_screen_names = [person_screen_name.get('screen_name') for person_screen_name in persons_screen_names] 

    for person_screen_name in persons_screen_names:
        settings.REDIS_INSTANCE.set(person_screen_name, mode_flag)

    if mode_flag:
        pool = mp.Pool(processes=4) 
        pool.map(v2_download_user, persons_screen_names)
        # for person_screen_name in persons_screen_names:
        #     v2_download_user(person_screen_name)