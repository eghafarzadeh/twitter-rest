# Created by elham at 11/28/20

# from django.contrib.auth.models import User
from rest_framework import serializers

from tweets.models import Tweet, Comment


class TweetSerializer(serializers.ModelSerializer):
    comments = serializers.StringRelatedField(many=True)
    text = serializers.CharField(
        required=True,
        max_length=256
    )

    def create(self, validated_data):
        tweet = Tweet(text=validated_data['text'])
        tweet.owner = validated_data['owner']
        tweet.save()
        return tweet

    class Meta:
        model = Tweet
        fields = ['id', 'text', 'owner', 'comments', 'updated_at']


class CommentSerializer(serializers.ModelSerializer):
    text = serializers.CharField(
        required=True,
        max_length=256
    )

    def create(self, validated_data):
        comment = Comment(text=validated_data['text'], owner=validated_data['owner'], tweet=validated_data['tweet'])
        # comment.owner = self.context["owner"]
        # comment.tweet = self.context["tweet"]
        comment.save()
        return comment

    class Meta:
        model = Comment
        fields = ('id', 'text', 'owner', 'tweet')
