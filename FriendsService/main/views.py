from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, generics
from django.contrib.auth.models import User

from .models import Friends, FriendshipRequests
from .serializers import FriendsSerializer, FriendshipRequestsSerializer


class FriendsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        friends = Friends.objects.all()
        serializer = FriendsSerializer(friends, many=True)
        return Response(serializer.data)


class RequestsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        request_list = FriendshipRequests.objects.all()
        serializer = FriendshipRequestsSerializer(request_list, many=True)
        return Response(serializer.data)




