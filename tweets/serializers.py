# Created by elham at 11/28/20

from rest_framework import serializers

from tweets.models import Tweet, Comment


class TweetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    comments = serializers.StringRelatedField(many=True, required=False)
    text = serializers.CharField(
        required=True,
        max_length=256
    )

    class Meta:
        model = Tweet
        fields = ['id', 'text', 'owner', 'comments', 'updated_at']


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    tweet = serializers.ReadOnlyField(source='tweet_id')
    text = serializers.CharField(
        required=True,
        max_length=256
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'owner', 'tweet')
