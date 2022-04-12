import csv


def save_tweets_to_csv(screen_name, tweets):
    with open(f'{screen_name}_tweets.csv', 'w',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(tweets)