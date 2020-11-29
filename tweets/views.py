# Create your views here.
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.custom_authentication import SafeJWTAuthentication
from accounts.models import CustomUser
from tweets.models import Tweet, Comment
from tweets.serializers import TweetSerializer, CommentSerializer
from twitter import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class TweetList(generics.ListAPIView):
    queryset = Tweet.objects.all().order_by("updated_at")
    serializer_class = TweetSerializer

    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TweetItem(APIView):
    """
    Creates the user.
    """
    authentication_classes = [TokenAuthentication, SafeJWTAuthentication]

    def post(self, request):
        data = request.data
        data["owner"] = request.user.id
        data["comments"] = []
        serializer = TweetSerializer(data=data)
        # todo
        if serializer.is_valid():
            tweet = serializer.save(owner=self.request.user)
            serializer = TweetSerializer(tweet)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get(self, request):
    #     """get tweets of all users"""
    #     tweets = Tweet.objects.all().order_by("updated_at")
    #     serializer = TweetSerializer(tweets, many=True)
    #     return JsonResponse(serializer.data, safe=False)


class TweetDetail(APIView):
    authentication_classes = [TokenAuthentication, SafeJWTAuthentication]

    def get(self, request, tweet_id):
        print(tweet_id)
        try:
            tweet = Tweet.objects.get(id=tweet_id)
        except Tweet.DoesNotExist:
            return JsonResponse({'message': 'The Tweet does not exist'}, status=status.HTTP_404_NOT_FOUND)
            # Make sure the tweet belongs to the current user.
        if tweet.owner != request.user:
            return Response({"error": "Tweet Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TweetSerializer(tweet)
        return JsonResponse(serializer.data)

    def delete(self, request, tweet_id):
        try:
            tweet = Tweet.objects.get(id=tweet_id)
        except Tweet.DoesNotExist:
            return JsonResponse({'message': 'The Tweet does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if tweet.owner != request.user:
            return Response({"error": "Tweet Not found"}, status=status.HTTP_404_NOT_FOUND)
        tweet.delete()
        return JsonResponse({'message': 'Tweet was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, tweet_id):
        try:
            tweet = Tweet.objects.get(id=tweet_id)
        except Tweet.DoesNotExist:
            return JsonResponse({'message': 'The Tweet does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if tweet.owner != request.user:
            return Response({"error": "Tweet Not found"}, status=status.HTTP_404_NOT_FOUND)

        tweet_data = JSONParser().parse(request)
        tutorial_serializer = TweetSerializer(tweet, data=tweet_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TweetUser(APIView):
    def get(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        tweets = Tweet.objects.all().filter(owner=user)
        serializer = TweetSerializer(tweets, many=True)
        return JsonResponse(serializer.data, safe=False)


class TweetComment(APIView):
    def post(self, request, tweet_id):
        """create a new comment for tweet with tweet id: tweet_id"""
        # todo
        data = request.data
        data['owner'] = request.user.id
        data['tweet'] = tweet_id
        # context = {"owner": request.user, "tweet": tweet}
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save()
            serializer = CommentSerializer(comment)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, tweet_id):
        """get comments of a tweet with tweet id: tweet_id"""
        comments = Comment.objects.all().filter(tweet=tweet_id)
        serializer = CommentSerializer(comments, many=True)
        return JsonResponse(serializer.data, safe=False)
