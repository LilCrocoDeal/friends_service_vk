from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token

from rest_framework.test import APITestCase
from rest_framework import status


class FriendsTest(APITestCase):

    def test_registration(self):
        response = self.client.post(reverse('registration'), data={
            'username': 'test', 'password': '12345'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test')

    def test_request_shaking(self):
        user1 = {'username': 'test1', 'password': '12345'}
        user2 = {'username': 'test2', 'password': '12345'}
        response1 = self.client.post(reverse('registration'), data=user1)
        response2 = self.client.post(reverse('registration'), data=user2)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(User.objects.count(), 1)
        # self.assertEqual(User.objects.get().username, 'test')

