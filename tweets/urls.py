# Created by elham at 11/28/20
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.TweetList.as_view(), name='tweet-list'),
    url(r'^(?P<pk>[0-9]+)$', views.TweetDetail.as_view(), name='tweet-detail'),
    url(r'^userId/(?P<user_id>[0-9]+)$', views.UserTweets.as_view(), name='user-tweet'),
    url(r'^(?P<tweet_id>[0-9]+)/comment$', views.CommentList.as_view(), name='tweet-comment2'),
]
