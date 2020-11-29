from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()


# Create your models here.
class CustomUser(AbstractUser):
    name = models.CharField(max_length=16)
    # created_at = models.DateField(default=timezone.now)
    # updated_at = models.AutoDateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
