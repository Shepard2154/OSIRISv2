from urllib.parse import urlparse


def get_domain(url):
    return urlparse(url).netloc


def get_user_mentions(tweet):
    result = ''
    mentions = tweet.entities.get('user_mentions')
    for mention in mentions:
        result += mention.get('screen_name') + ' '
    return result


def get_hashtags(tweet):
    result = ''
    hashtags = tweet.entities.get('hashtags')
    for hashtag in hashtags:
        result += hashtag.get('text') + ' '
    return result


def get_urls(tweet):
    result = ''
    urls = tweet.entities.get('urls')
    for url in urls:
        result += url.get('expanded_url') + ';'
    return result


def get_media_url(tweet):
    try:
        return tweet.entities.media.get('media_url')
    except Exception:
        return ''
