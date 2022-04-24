import json
from celery import shared_task
from django.conf import settings
from loguru import logger
import multiprocessing as mp

from .models import TwitterHashtags
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