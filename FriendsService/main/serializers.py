from abc import ABC

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Friends, FriendshipRequests


class FriendsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Friends
        field = ("first_user", "second_user")


class FriendshipRequestsSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendshipRequests
        field = ("to_user", "from_user", "status")



