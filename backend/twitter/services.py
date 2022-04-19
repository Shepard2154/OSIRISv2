from pathlib import Path

import pandas as pd

from .models import TwitterHashtags


BASE_DIR = Path(__file__).resolve().parent.parent

def get_hashtags_from_file():
    hashtags_df = pd.read_excel('static/hashtags.xlsx', usecols=[0,2,4,6,8], na_filter=False)
    hashtags_df.dropna(inplace=True)
    hashtags = hashtags_df.to_dict('list')

    all_hashtags = []
    for hashtag_class in hashtags:
        all_hashtags.extend([hashtag_item[1:] for hashtag_item in hashtags.get(hashtag_class) if hashtag_item])
    all_hashtags = list(set(all_hashtags))

    for hashtag in all_hashtags:
        TwitterHashtags.objects.update_or_create(hashtag_value=hashtag)
    return all_hashtags