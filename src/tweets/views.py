# Create your views here.
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from accounts.custom_authentication import SafeJWTAuthentication
from accounts.models import CustomUser
from tweets.models import Tweet, Comment
from tweets.permissions import IsOwnerOrReadOnly
from tweets.serializers import TweetSerializer, CommentSerializer
from twitter import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class TweetList(generics.ListCreateAPIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,)

    authentication_classes = [TokenAuthentication, SafeJWTAuthentication]

    queryset = Tweet.objects.all().order_by("updated_at")
    serializer_class = TweetSerializer

    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TweetDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,)

    authentication_classes = [TokenAuthentication, SafeJWTAuthentication]

    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer


class UserTweets(APIView):
    def get(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        tweets = Tweet.objects.all().filter(owner=user)
        serializer = TweetSerializer(tweets, many=True)
        return JsonResponse(serializer.data, safe=False)


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_url_kwarg = "tweet_id"

    def get_queryset(self):
        tweet_id = self.kwargs.get(self.lookup_url_kwarg)
        comments = Comment.objects.filter(tweet=tweet_id)
        return comments

    def perform_create(self, serializer):
        tweet_id = self.kwargs.get(self.lookup_url_kwarg)
        serializer.save(owner=self.request.user, tweet_id=tweet_id)
