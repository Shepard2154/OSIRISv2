from datetime import datetime

from multiprocessing import AuthenticationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import login, logout
from rest_framework.generics import (
    CreateAPIView, 
    RetrieveAPIView, 
    UpdateAPIView, 
    DestroyAPIView, 
    ListAPIView,
)
from .serializers import (
    TweetListSerializer,
    UserCreateSerializer, 
    UserDetailSerializer, 
    UserListSerializer,
    RegistrationSerializer,
    LoginSerializer,
    UserRetrieveSerializer,

    TweetCreateSerializer,
)
from .services import (
    get_user_info,
    get_all_tweets, 
)
from .models import TwitterUserInfo
from .models import TwitterTweet


class RegistrationAPIView(APIView):
    """
    Registers a new user.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        Creates a new User object.
        Username, email and password are required.
        Returns a JSON web token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                'username': serializer.data.get('username')
            }
        )


class LoginAPIView(APIView):
    """
    Logs in an existing user.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Checks is user exists.
        Email and password are required.
        Returns a JSON web token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        user =  serializer.validated_data['user']

        login(request, user)

        return Response(
            {
                'token': token
            }
        )


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        logout(request)
        return Response()


class UserCreateAPIView(CreateAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = TwitterUserInfo.objects.all()
    serializer_class = UserCreateSerializer


class UserDetailAPIView(RetrieveAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = TwitterUserInfo.objects.all()
    serializer_class = UserDetailSerializer

    
class UserRetrieveAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserRetrieveSerializer

    def get(self, request, screen_name):
        desired_user = TwitterUserInfo.objects.get(screen_name=screen_name).__dict__
        serializer = self.serializer_class(data=desired_user)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data)
    

class UserUpdateAPIView(UpdateAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = TwitterUserInfo.objects.all()
    serializer_class = UserDetailSerializer


class UserDeleteAPIView(DestroyAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = TwitterUserInfo.objects.all()
    serializer_class = UserDetailSerializer

class UserListAPIView(ListAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = TwitterUserInfo.objects.all()
    serializer_class = UserListSerializer


class DownloadUserInfo(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated] 
    serializer_class = UserRetrieveSerializer

    def get(self, request, screen_name):
        get_user_info(screen_name)
        desired_user = TwitterUserInfo.objects.get(screen_name=screen_name).__dict__
        # удалить костыли к production 
        desired_user['updated_at'] = datetime.now()
        desired_user['location'] = 'undefined'
        desired_user['url'] = 'underfined'
        # удалить костыли к production
        serializer = self.serializer_class(data=desired_user)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data)

class TweetCreateAPIView(CreateAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = TwitterTweet.objects.all()
    serializer_class = TweetCreateSerializer


class DownloadTweets(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TweetCreateSerializer

    def get(self, request, screen_name):
        tweets = get_all_tweets(screen_name)
        for tweet in tweets:
            serializer = self.serializer_class(data=tweet)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        all_tweets_of_user = TwitterTweet.objects.all()
        serializer = TweetListSerializer(data=all_tweets_of_user.__dict__)
        serializer.is_valid(raise_exception=True) 
        
        data = serializer.data
        print('data!: ', data)
        print('sasadasdsadas')
        # dates = get_tweet_dates(tweets)
        # weekdays = get_tweet_weekday(tweets) 
        # time = get_tweet_time(tweets)
        
        return Response(data)