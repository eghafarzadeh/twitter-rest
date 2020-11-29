# Created by elham at 11/28/20

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from accounts.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=32,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    name = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(min_length=6, max_length=100,
                                     write_only=True)

    def create(self, validated_data):
        user = CustomUser(username=validated_data['username'],
                          name=validated_data['name'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'name', 'password')


class UpdateUserNameSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=100)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'name')

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
