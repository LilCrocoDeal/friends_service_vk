from django.contrib.auth import logout
from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from django.db.models import Q

from .models import Friends, FriendshipRequests
from .serializers import FriendsSerializer, FriendshipRequestsSendSerializer, \
    RequestsSerializer, RequestsManageSerializer, FriendsDeleteSerializer, \
    CreateUserSerializer, RequestsDeleteSerializer, LoginUserSerializer


class RegistrationView(APIView):

    @swagger_auto_schema(
        operation_description="Register user to service.",
        request_body=CreateUserSerializer(),
        responses={201: CreateUserSerializer(),
                   400: "Invalid data"}
    )
    def post(self, request):
        message = CreateUserSerializer(data=request.data)
        if message.is_valid():
            username = message.validated_data["username"]
            password = message.validated_data["password"]
            message.save()
            return Response({"username": username, "password": password}, status=201)
        return Response({"detail": "Invalid data"}, status=400)


class LoginView(APIView):

    @swagger_auto_schema(
        operation_description="Obtain token to authenticate user.",
        request_body=LoginUserSerializer(),
        responses={200: LoginUserSerializer(),
                   400: "Invalid data"}
    )
    def post(self, request):
        message = LoginUserSerializer(data=request.data)
        if message.is_valid():
            if message.second_validation():
                user = User.objects.get(username=message.validated_data.get("username"))
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=200)
        return Response({"detail": "Invalid data"}, status=400)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Logout authenticated user.",
        responses={200: "Success",
                   401: "Error: Unauthorized"}
    )
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({"detail": "Success"}, status=200)


class FriendsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get a list of current friends.",
        responses={200: FriendsSerializer(many=True),
                   401: "Error: Unauthorized"}
    )
    def get(self, request):
        friends = Friends.objects.filter(core_person=request.user)
        serializer = FriendsSerializer(friends, many=True)
        return Response(serializer.data)


class FriendsDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Delete one of your friends by username.",
        request_body=FriendsDeleteSerializer(),
        responses={200: "The user has been successfully removed from friends",
                   401: "Error: Unauthorized",
                   400: "You can't remove yourself from your friends\nThis user is not exist\n"
                        "You are not friends with this user"}
    )
    def delete(self, request):
        message = FriendsDeleteSerializer(data=request.data)
        if message.is_valid():
            username = message.validated_data.get("username")
            if username == request.user.username:
                return Response({"detail": "You can't remove yourself from your friends"}, status=400)
            if not len(User.objects.filter(username=username)):
                return Response({"detail": "This user is not exist"}, status=400)
            elif not len(Friends.objects.filter(core_person=request.user, friend=username)):
                return Response({"detail": "You are not friends with this user"}, status=400)
            else:
                Friends.objects.get(core_person=request.user, friend=username).delete()
                Friends.objects.get(core_person=username, friend=request.user).delete()
                FriendshipRequests.objects.create(to_user=request.user,
                                                  from_user=username, status="rejected by receiver")
                return Response({"detail": "The user has been successfully removed from friends"}, status=200)
        return Response(message.error, status=400)


class RequestsSendView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Send friend request to existing user. In the field "
                              "\"to_user\" write down the chosen user's name",
        request_body=FriendshipRequestsSendSerializer(),
        responses={200: "The request has been sent",
                   401: "Error: Unauthorized",
                   400: "You are trying to add yourself as a friend\n"
                        "You are trying to add a non-existent user as a friend\n"
                        "You have already sent a friend request to this user\n"
                        "You and the user are already friends"}
    )
    def post(self, request):
        message = FriendshipRequestsSendSerializer(data=request.data)
        if message.is_valid():
            if message.second_validation(request.user):
                message.save(from_user=request.user)
                return Response({"detail": "The request has been sent"}, status=200)
        return Response(message.error, status=400)


class RequestsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get a list of requests sent by you/to you.",
        responses={200: RequestsSerializer(many=True),
                   401: "Error: Unauthorized"}
    )
    def get(self, request):
        request_list = FriendshipRequests.objects.filter(Q(to_user=request.user) | Q(from_user=request.user))
        serializer = RequestsSerializer(request_list, many=True)
        return Response(serializer.data)


class RequestsManageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Accept or reject request from chosen user. To accept request write "
                              "down \"1\" in the field \"decision\", to reject - \"0\". In the field "
                              "\"request_sender\" write down the chosen user's name.",
        request_body=RequestsManageSerializer(),
        responses={201: "The user has been added to your friends",
                   200: "The user's request was rejected",
                   401: "Error: Unauthorized",
                   400: "Invalid data"}
    )
    def post(self, request):
        message = RequestsManageSerializer(data=request.data)
        if message.is_valid() and len(FriendshipRequests.objects.filter(
                from_user=message.validated_data.get("request_sender"), to_user=request.user)) > 0:

            if message.validated_data.get("decision"):
                FriendshipRequests.objects.get(from_user=message.validated_data.get("request_sender"),
                                               to_user=request.user).delete()
                Friends.objects.create(core_person=request.user,
                                       friend=message.validated_data.get("request_sender"))
                Friends.objects.create(core_person=message.validated_data.get("request_sender"),
                                       friend=request.user)
                return Response({"detail": "The user has been added to your friends"}, status=201)
            elif not message.validated_data.get("decision"):
                current = FriendshipRequests.objects.get(from_user=message.validated_data.get("request_sender"),
                                                         to_user=request.user)
                current.status = "rejected by receiver"
                current.save()
                return Response({"detail": "The user's request was rejected"}, status=200)
        return Response(message.error, status=400)


class RequestsDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Delete one of the friend request was sent to you.",
        request_body=RequestsDeleteSerializer(),
        responses={200: "The request has been successfully removed",
                   401: "Error: Unauthorized",
                   400: "Invalid data"}
    )
    def delete(self, request):
        message = RequestsDeleteSerializer(data=request.data)
        if message.is_valid():
            username = message.validated_data.get("from_user")
            if not len(FriendshipRequests.objects.filter(to_user=request.user, from_user=username)):
                return Response(message.error, status=400)
            else:
                FriendshipRequests.objects.get(to_user=request.user, from_user=username).delete()
                return Response({"detail": "The request has been successfully removed"}, status=200)
        return Response(message.error, status=400)


class InfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    query_param = openapi.Parameter("username", openapi.IN_QUERY, description="username", type=openapi.TYPE_STRING)

    @swagger_auto_schema(
        manual_parameters=[query_param],
        operation_description="Get information about your relationship with the requested user.",
        responses={200: "This user is you\nThis user has sent you a friend request\n"
                        "You have sent this user a friend request\nYou are friends with this user\n"
                        "You don't have any interactions with this user",
                   401: "This user is not exist"}
    )
    def get(self, request):
        username = request.query_params.get("username")
        if not len(User.objects.filter(username=username)):
            return Response({"detail": "This user is not exist"}, status=400)
        elif username == request.user.username:
            return Response({"detail": "This user is you"}, status=200)
        elif len(FriendshipRequests.objects.filter(to_user=request.user, from_user=username)) > 0:
            return Response({"detail": "This user has sent you a friend request"}, status=200)
        elif len(FriendshipRequests.objects.filter(to_user=username, from_user=request.user)) > 0:
            return Response({"detail": "You have sent this user a friend request"}, status=200)
        elif len(Friends.objects.filter(core_person=request.user, friend=username)) > 0:
            return Response({"detail": "You are friends with this user"}, status=200)
        else:
            return Response({"detail": "You don't have any interactions with this user"}, status=200)
