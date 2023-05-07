from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from .models import Friends, FriendshipRequests
from .serializers import FriendsSerializer, FriendshipRequestsSendSerializer, FriendshipRequestsGetSerializer


class FriendsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        friends = Friends.objects.filter(core_person=request.user)
        serializer = FriendsSerializer(friends, many=True)
        return Response(serializer.data)


class RequestsSendView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        message = FriendshipRequestsSendSerializer(data=request.data)
        if message.is_valid():
            if message.second_validation(request.user):
                message.save(from_user=request.user)
                return Response('Заявка была отправлена', status=201)
        return Response(message.error, status=400)


class RequestsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        request_list = FriendshipRequests.objects.filter(to_user=request.user)
        serializer = FriendshipRequestsGetSerializer(request_list, many=True)
        return Response(serializer.data)
