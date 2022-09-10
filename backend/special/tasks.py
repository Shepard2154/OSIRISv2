import multiprocessing as mp

from celery import shared_task
from .celery import *
from celery.contrib.abortable import AbortableTask
from django.conf import settings
from loguru import logger

from .models import Hashtags, Users
from .services import *


logger.add("static/logs/special_tasks.log", format="{time} {message}", level="DEBUG", rotation="500 MB", compression="zip", encoding='utf-8')


@app.task(bind=True, base=AbortableTask, time_limit=31536000)
def scrape_hashtags(self, hashtags_values, name):
    for hashtag_value in hashtags_values:
        v2_download_tweets_by_hashtag(hashtag_value, name)


@app.task(bind=True, base=AbortableTask, time_limit=31536000)
def scrape_limit_hashtags(self, hashtags_values, max_count=1000):
    for hashtag_value in hashtags_values:
        v2_download_tweets_by_hashtag_and_limit(hashtag_value, max_count)


@app.task(bind=True, base=AbortableTask, time_limit=31536000)
def scrape_persons(self, persons_screen_names):
    for person_screen_name in persons_screen_names:
        v2_download_user(person_screen_name)