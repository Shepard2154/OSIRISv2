from datetime import datetime


def from_v2_tweet(tweet):
    urls = []
    if tweet.get('outlinks'):
        urls += tweet.get('outlinks')
        if tweet.get('tcooutlinks'):
            urls += tweet.get('tcooutlinks')

    id = tweet.get('id')
    created = tweet.get('date')
    text = tweet.get('content')
    lang = tweet.get('lang')
    source = tweet.get('sourceLabel')

    author_id = tweet.get('user').get('id')
    author_screen_name = tweet.get('user').get('username')

    reply_count = tweet.get('replyCount')
    retweet_count = tweet.get('retweetCount')
    quote_count = tweet.get('quoteCount')
    likes_count = tweet.get('likeCount')

    original_screen_name = tweet.get('inReplyToUser').get('username') if tweet.get('inReplyToUser') else ''
    retweet_created = datetime(2006, 3, 1, 0, 0, 0, 0)
    retweet_id = tweet.get('inReplyToTweetId')

    hashtags = tweet.get('hashtags')
    user_mentions = tweet.get('mentionedUsers')
    coordinates = tweet.get('coordinates')

    updated_at = datetime.now()

    valid_tweet = {
        'id': id,
        'created': created,
        'text': text,
        'lang': lang,
        'source': source,
        'author_id': author_id,
        'author_screen_name': author_screen_name,
        'reply_count': reply_count,
        'retweet_count': retweet_count,
        'quote_count': quote_count,
        'likes_count': likes_count,
        'original_screen_name': original_screen_name,
        'retweet_created': retweet_created,
        'retweet_id': retweet_id,
        'hashtags': hashtags,
        'urls': urls,
        'user_mentions': user_mentions,
        'coordinates': coordinates,
        'updated_at': updated_at
    }

    return valid_tweet


def from_v2_user(user):
    valid_user = {}
    valid_user['id'] = user.get('id')
    valid_user['screen_name'] = user.get('username')
    valid_user['name'] = user.get('displayname')
    valid_user['twitter_url'] = f"https://twitter.com/{valid_user.get('screen_name')}"
    valid_user['profile_image_url'] = user.get('profileImageUrl')
    valid_user['description'] = user.get('description')
    valid_user['description_urls'] = user.get('descriptionUrls')
    valid_user['hashtags'] = []
    valid_user['birthday'] = datetime(2006, 3, 1, 0, 0, 0, 0)
    valid_user['created'] = user.get('created')
    valid_user['web'] = user.get('linkUrl')
    valid_user['location'] = user.get('location')
    valid_user['category'] = user.get('label')
    valid_user['followers_count'] = user.get('followersCount')
    valid_user['friends_count'] = user.get('friendsCount')
    valid_user['likes_count'] = user.get('favouritesCount')
    valid_user['statuses_count'] = user.get('statusesCount')
    valid_user['listed_count'] = user.get('listedCount')
    valid_user['updated_at'] = datetime.now()

    return valid_user