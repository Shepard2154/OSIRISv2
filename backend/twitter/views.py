from datetime import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from multiprocessing import AuthenticationError
import statistics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView, 
)

from .v1_services import *
from .statistics import calculate_tweets_type
from .serializers import *
from .models import TwitterUserInfo, TwitterTweet
from .cli import download_mytweets

class TweetCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    
    queryset = TwitterTweet.objects.all()
    serializer_class = TweetCreateSerializer


class DownloadPersonInfo(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRetrieveSerializer

    def get(self, request, screen_name):
        get_user_info(screen_name)
        desired_user = TwitterUserInfo.objects.get(screen_name=screen_name).__dict__
        serializer = self.serializer_class(data=desired_user)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data)


class DownloadTweets(APIView):
    permission_classes = [AllowAny]
    serializer_class = TweetListSerializer

    def get(self, request, screen_name):
        tweets = download_all_tweets(screen_name)
        save_tweets(tweets)

        user_id = TwitterUserInfo.objects.get(screen_name=screen_name).id
        tweets = TwitterTweet.objects.all().filter(user_id=user_id)
        serializer = self.serializer_class(instance=tweets, many=True)
        
        return Response(serializer.data)


class V1_DownloadTweet(APIView):
    permission_classes = [AllowAny]

    def get(self, request, tweet_id):
        tweet = v1_get_tweet_by_id(tweet_id)._json
        
        return Response(tweet)


# class V2_DownloadTweetsByHashtag(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request, hashtag_value):
#         tweet = download_tweets(hashtag_value)
        
#         return Response(tweet[0])


class CalculateTweetsStatistics(APIView):
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    serializer_class = TweetListStatistics

    def get(self, request, screen_name):
        statistics = get_tweets_statistics(screen_name)
        print(statistics)
        
        return Response('Ok')
        # quotes = models.JSONField(null=True)
        # retweets = models.JSONField(null=True)

        # serializer = self.serializer_class(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()



class MessageSendAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, hashtag_value, power):
        if power == 'open':
            channel_layer = get_channel_layer()
            for tweet in download_mytweets(hashtag_value):
                async_to_sync(channel_layer.group_send)(
                    "general", {"type": "get_tweets", "text": tweet}
                )
            return Response({"status": True}, status=status.HTTP_200_OK)
            
        elif power == 'close':
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "general", {"type": "close_scraper", "text": 'done'}
            )
            return Response({"status": True}, status=status.HTTP_200_OK)