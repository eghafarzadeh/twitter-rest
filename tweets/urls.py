# Created by elham at 11/28/20
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.TweetListCreate.as_view(), name='tweet-list-create'),
    url(r'^create$', views.TweetItem.as_view(), name='tweet-item'),
    url(r'^userId/(?P<user_id>[0-9]+)$', views.TweetUser.as_view(), name='tweet-user'),
    url(r'^(?P<tweet_id>[0-9]+)$', views.TweetDetail.as_view(), name='tweet-detail'),
    url(r'^(?P<tweet_id>[0-9]+)/comment$', views.TweetComment.as_view(), name='tweet-comment'),
]
