from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import (
    CreateAPIView, 
    RetrieveAPIView, 
    UpdateAPIView, 
    DestroyAPIView, 
    ListAPIView,
)
from .serializers import (
    UserCreateSerializer, 
    UserDetailSerializer, 
    UserListSerializer,
    RegistrationSerializer,
    LoginSerializer,
)
from .services import (
    get_all_tweets, 
    get_tweet_dates, 
    get_tweet_time, 
    get_tweet_weekday,
)
from .models import TwitterUserInfo


class UserCreateAPIView(CreateAPIView):
    queryset = TwitterUserInfo.objects.all()
    serializer_class = UserCreateSerializer


class UserDetailAPIView(RetrieveAPIView):
    queryset = TwitterUserInfo.objects.all()
    serializer_class = UserDetailSerializer


class UserUpdateAPIView(UpdateAPIView):
    queryset = TwitterUserInfo.objects.all()
    serializer_class = UserDetailSerializer


class UserDeleteAPIView(DestroyAPIView):
    queryset = TwitterUserInfo.objects.all()
    serializer_class = UserDetailSerializer

class UserListAPIView(ListAPIView):
    queryset = TwitterUserInfo.objects.all()
    serializer_class = UserListSerializer


class download_tweets(APIView):
    def post(self, request):
        screen_name = request.data.get('screen_name')
        print(screen_name)
        tweets = get_all_tweets(screen_name)

        dates = get_tweet_dates(tweets)
        weekdays = get_tweet_weekday(tweets) 
        time = get_tweet_time(tweets)

        return (Response({"tweets": {"dates": dates, "time": time, "weekdays": weekdays}}))
        # # Create an article from the above data
        # serializer = ArticleSerializer(data=article)
        # if serializer.is_valid(raise_exception=True):
        #     article_saved = serializer.save()
        # return Response({"success": "Article '{}' created successfully".format(article_saved.title)})

class RegistrationAPIView(APIView):
    """
    Registers a new user.
    """
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        Creates a new User object.
        Username, email, and password are required.
        Returns a JSON web token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                'token': serializer.data.get('token', None),
            }
        )


class LoginAPIView(APIView):
    """
    Logs in an existing user.
    """
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

        return Response(serializer.data)