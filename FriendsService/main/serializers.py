from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Friends, FriendshipRequests


class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = ("friend",)


class FriendshipRequestsSendSerializer(serializers.ModelSerializer):
    error = ''

    class Meta:
        model = FriendshipRequests
        fields = ("to_user", "status",)

    def second_validation(self, user):
        if self.validated_data.get("to_user") == str(user):
            self.error = 'Вы пытаетесь добавить в друзья самого себя'
            return False
        if len(User.objects.filter(username=self.validated_data.get("to_user"))) == 0:
            self.error = 'Вы пытаетесь добавить в друзья несуществующего пользователя'
            return False

        if len(FriendshipRequests.objects.filter(from_user=user,
                                                 to_user=self.validated_data.get("to_user"))) > 0:
            self.error = 'Вы уже отправляли заявку в друзья этому пользователю'
            return False

        if len(Friends.objects.filter(core_person=user,
                                      friend=self.validated_data.get("to_user"))) > 0:
            self.error = 'Вы с пользователем и так находитесь в друзьях'
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


class FriendshipRequestsGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendshipRequests
        fields = ("from_user", "status",)
