import json
from celery import shared_task
from django.conf import settings
from loguru import logger
import multiprocessing as mp

from .models import TwitterHashtags, TwitterPersons
from .services import *

logger.add("logs/twitter_tasks.log", format="{time} {message}", level="DEBUG", rotation="500 MB", compression="zip", encoding='utf-8')

@shared_task(bind=True)
def example(self, msg):
    logger.info(msg)


@shared_task(bind=True)
def scrape_hashtags(self, hashtags_values, all_flag, mode_flag):
    if all_flag:
        hashtags_values = TwitterHashtags.objects.all().values('hashtag_value')
        hashtags_values = [hashtag.get('hashtag_value') for hashtag in hashtags_values] 

    for hashtag_value in hashtags_values:
        settings.REDIS_INSTANCE.set(hashtag_value, mode_flag)

    if mode_flag:
        pool = mp.Pool(processes=4) 
        pool.map(v2_download_tweets_by_hashtag, hashtags_values)


@shared_task(bind=True)
def scrape_persons(self, persons_screen_names, all_flag, mode_flag):
    if all_flag:
        persons_screen_names = TwitterPersons.objects.all().values('person_screen_name')
        persons_screen_names = [person_screen_name.get('person_screen_name') for person_screen_name in persons_screen_names] 

    for person_screen_name in persons_screen_names:
        settings.REDIS_INSTANCE.set(person_screen_name, mode_flag)

    if mode_flag:
        pool = mp.Pool(processes=4) 
        pool.map(v2_download_username, persons_screen_names)