from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token

from rest_framework.test import APITestCase, APIClient
from rest_framework import status


class FriendsTest(APITestCase):

    def setUp(self):
        user = User.objects.create(username='prihlop', password='12345')
        client = APIClient()
        response = self.client.post(reverse('authtoken'), json={'username': 'prihlop', 'password': '12345'})
        print(response.json())

    def test_get_friends_test(self):
        request = self.client.get(reverse('friends'), [])
        print(request.json())

