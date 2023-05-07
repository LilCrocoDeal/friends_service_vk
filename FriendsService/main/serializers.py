from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Friends, FriendshipRequests


class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = ("friend",)


class FriendsDeleteSerializer(serializers.Serializer):
    username = serializers.CharField()
    error = 'Invalid data'


class FriendshipRequestsSendSerializer(serializers.ModelSerializer):
    error = 'Invalid data'

    class Meta:
        model = FriendshipRequests
        fields = ("to_user", "status",)

    def second_validation(self, user):
        if self.validated_data.get("to_user") == str(user):
            self.error = 'Are you trying to add yourself as a friend'
            return False
        if not len(User.objects.filter(username=self.validated_data.get("to_user"))):
            self.error = 'You are trying to add a non-existent user as a friend'
            return False

        if len(FriendshipRequests.objects.filter(from_user=user,
                                                 to_user=self.validated_data.get("to_user"))) > 0:
            self.error = 'You have already sent a friend request to this user'
            return False

        if len(Friends.objects.filter(core_person=user,
                                      friend=self.validated_data.get("to_user"))) > 0:
            self.error = 'You and the user are already friends'
            return False

        return True

    def create(self, validated_data):
        if len(FriendshipRequests.objects.filter(from_user=validated_data.get("to_user"),
                                                 to_user=validated_data.get("from_user"))) > 0:
            FriendshipRequests.objects.get(from_user=validated_data.get("to_user"),
                                           to_user=validated_data.get("from_user")).delete()
            new_friend = Friends.objects.create(core_person=validated_data.get("from_user"),
                                                friend=validated_data.get("to_user"))
            Friends.objects.create(core_person=validated_data.get("to_user"),
                                   friend=validated_data.get("from_user"))
            return new_friend

        else:
            new_request = FriendshipRequests.objects.create(to_user=validated_data.get("to_user"),
                                                            from_user=validated_data.get("from_user"))
            return new_request


class RequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendshipRequests
        fields = ("from_user", "to_user", "status",)


class RequestManageSerializer(serializers.Serializer):
    decision = serializers.BooleanField()
    request_sender = serializers.CharField()
    error = 'Invalid data'



