from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from django.db.models import Q

from .models import Friends, FriendshipRequests
from .serializers import FriendsSerializer, FriendshipRequestsSendSerializer, \
    RequestsSerializer, RequestManageSerializer, FriendsDeleteSerializer


class FriendsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        friends = Friends.objects.filter(core_person=request.user)
        serializer = FriendsSerializer(friends, many=True)
        return Response(serializer.data)


class FriendsDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        message = FriendsDeleteSerializer(data=request.data)
        if message.is_valid():
            username = message.validated_data.get("username")
            if username == request.user.username:
                return Response("You can't remove yourself from your friends", status=400)
            if not len(User.objects.filter(username=username)):
                return Response("This user is not exist", status=400)
            elif not len(Friends.objects.filter(core_person=request.user, friend=username)):
                return Response("You are not friends with this user", status=400)
            else:
                Friends.objects.get(core_person=request.user, friend=username).delete()
                Friends.objects.get(core_person=username, friend=request.user).delete()
                FriendshipRequests.objects.create(to_user=request.user,
                                                  from_user=username, status="rejected by receiver")
                return Response("The user has been successfully removed from friends", status=201)
        return Response(message.error, status=400)


class RequestsSendView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        message = FriendshipRequestsSendSerializer(data=request.data)
        if message.is_valid():
            if message.second_validation(request.user):
                message.save(from_user=request.user)
                return Response("The request has been sent", status=201)
        return Response(message.error, status=400)


class RequestsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        request_list = FriendshipRequests.objects.filter(Q(to_user=request.user) | Q(from_user=request.user))
        serializer = RequestsSerializer(request_list, many=True)
        return Response(serializer.data)


class RequestsManageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        message = RequestManageSerializer(data=request.data)
        if message.is_valid() and len(FriendshipRequests.objects.filter(
                from_user=message.validated_data.get("request_sender"), to_user=request.user)) > 0:

            if message.validated_data.get("decision"):
                FriendshipRequests.objects.get(from_user=message.validated_data.get("request_sender"),
                                               to_user=request.user).delete()
                Friends.objects.create(core_person=request.user,
                                       friend=message.validated_data.get("request_sender"))
                Friends.objects.create(core_person=message.validated_data.get("request_sender"),
                                       friend=request.user)
                return Response("The user has been added to your friends", status=201)
            elif not message.validated_data.get("decision"):
                current = FriendshipRequests.objects.get(from_user=message.validated_data.get("request_sender"),
                                                         to_user=request.user)
                current.status = "rejected by receiver"
                current.save()
                return Response("The user's request was rejected", status=201)
        return Response(message.error, status=400)


class InfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        username = request.query_params.get("username")
        if not len(User.objects.filter(username=username)):
            return Response("This user is not exist", status=400)
        elif username == request.user.username:
            return Response("This user is you", status=201)
        elif len(FriendshipRequests.objects.filter(to_user=request.user, from_user=username)) > 0:
            return Response("This user has sent you a friend request", status=201)
        elif len(FriendshipRequests.objects.filter(to_user=username, from_user=request.user)) > 0:
            return Response("You have sent this user a friend request", status=201)
        elif len(Friends.objects.filter(core_person=request.user, friend=username)) > 0:
            return Response("You are friends with this user", status=201)
        else:
            return Response("You don't have any interactions with this user", status=201)
