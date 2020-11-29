from django.db import models

# todo: check if there is a central solution for created_at and updated_at
from accounts.models import CustomUser


class Tweet(models.Model):
    text = models.CharField(max_length=256)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.text[:50]}..."


class Comment(models.Model):
    text = models.CharField(max_length=256)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.text[:50]}..."
