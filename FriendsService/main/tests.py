from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status


class TwoUsersTests(APITestCase):

    def preparation(self):
        user1 = {'username': 'test1', 'password': '12345'}
        user2 = {'username': 'test2', 'password': '12345'}
        self.client.post(reverse('registration'), data=user1)
        self.client.post(reverse('registration'), data=user2)

        user1_token = 'Token ' + self.client.post(reverse('login'), data=user1).data['token']
        user2_token = 'Token ' + self.client.post(reverse('login'), data=user2).data['token']

        return user1_token, user2_token

    def test_registration(self):
        response = self.client.post(reverse('registration'), data={'username': 'test', 'password': '12345'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test')

    def test_request_shaking(self):
        user1_token, user2_token = self.preparation()

        friends_first_user = self.client.get(reverse('friends'), headers={'Authorization': user1_token})
        self.assertEqual(friends_first_user.status_code, status.HTTP_200_OK)
        self.assertEqual(friends_first_user.data, [])

        request_first_user = self.client.post(reverse('requests_send'), data={
            'to_user': 'test2'
        }, headers={'Authorization': user1_token})
        self.assertEqual(request_first_user.status_code, status.HTTP_201_CREATED)

        request_second_user = self.client.post(reverse('requests_send'), data={
            'to_user': 'test1'
        }, headers={'Authorization': user2_token})
        self.assertEqual(request_second_user.status_code, status.HTTP_201_CREATED)

        friends_second_user = self.client.get(reverse('friends'), headers={'Authorization': user2_token})
        self.assertEqual(friends_second_user.status_code, status.HTTP_200_OK)
        self.assertEqual(friends_second_user.json(), [{'friend': 'test1'}])

    def test_add_delete_friends(self):
        user1_token, user2_token = self.preparation()

        self.client.post(reverse('requests_send'), data={
            'to_user': 'test2'
        }, headers={'Authorization': user1_token})

        self.client.post(reverse('requests_manage'), data={
            'decision': True, 'request_sender': 'test1'
        }, headers={'Authorization': user2_token})

        check_requests_second_user = self.client.get(reverse('requests'), headers={'Authorization': user2_token})
        self.assertEqual(check_requests_second_user.json(), [])

        check_friends_second_user = self.client.get(reverse('friends'), headers={'Authorization': user2_token})
        self.assertEqual(check_friends_second_user.json(), [{'friend': 'test1'}])

        self.client.delete(reverse('friends_delete'), data={
            'username': 'test1'
        }, headers={'Authorization': user2_token})

        check_requests_second_user_2 = self.client.get(reverse('requests'), headers={'Authorization': user2_token})
        self.assertEqual(check_requests_second_user_2.json(), [
            {'from_user': 'test1', 'to_user': 'test2', 'status': 'rejected by receiver'}
        ])

        check_friends_first_user = self.client.get(reverse('friends'), headers={'Authorization': user1_token})
        self.assertEqual(check_friends_first_user.json(), [])

        send_repeated_request_first_user = self.client.post(reverse('requests_send'), data={
            'to_user': 'test2'
        }, headers={'Authorization': user1_token})
        self.assertEqual(send_repeated_request_first_user.status_code, status.HTTP_400_BAD_REQUEST)


class FiveUsersTests(APITestCase):

    def preparation(self):
        user = {'username': 'user', 'password': '12345'}
        friend = {'username': 'friend', 'password': '12345'}
        requested = {'username': 'requested', 'password': '12345'}
        simp = {'username': 'simp', 'password': '12345'}
        noname = {'username': 'noname', 'password': '12345'}

        self.client.post(reverse('registration'), data=user)
        self.client.post(reverse('registration'), data=friend)
        self.client.post(reverse('registration'), data=requested)
        self.client.post(reverse('registration'), data=simp)
        self.client.post(reverse('registration'), data=noname)

        user_token = 'Token ' + self.client.post(reverse('login'), data=user).data['token']
        friend_token = 'Token ' + self.client.post(reverse('login'), data=friend).data['token']
        requested_token = 'Token ' + self.client.post(reverse('login'), data=requested).data['token']
        simp_token = 'Token ' + self.client.post(reverse('login'), data=simp).data['token']
        noname_token = 'Token ' + self.client.post(reverse('login'), data=noname).data['token']

        return user_token, friend_token, requested_token, simp_token, noname_token

    def test_get_all_info_cases(self):

        user_token, friend_token, _, simp_token, _ = self.preparation()

        self.client.post(reverse('requests_send'), data={'to_user': 'friend'}, headers={'Authorization': user_token})
        self.client.post(reverse('requests_send'), data={'to_user': 'requested'}, headers={'Authorization': user_token})
        self.client.post(reverse('requests_send'), data={'to_user': 'user'}, headers={'Authorization': friend_token})
        self.client.post(reverse('requests_send'), data={'to_user': 'user'}, headers={'Authorization': simp_token})

        self_info = self.client.get(reverse('info'), {'username': 'user'},
                                    headers={'Authorization': user_token})
        self.assertEqual(self_info.json(), {'detail': 'This user is you'})

        friend_info = self.client.get(reverse('info'), {'username': 'friend'},
                                      headers={'Authorization': user_token})
        self.assertEqual(friend_info.json(), {'detail': 'You are friends with this user'})

        requested_info = self.client.get(reverse('info'), {'username': 'requested'},
                                         headers={'Authorization': user_token})
        self.assertEqual(requested_info.json(), {'detail': 'You have sent this user a friend request'})

        simp_info = self.client.get(reverse('info'), {'username': 'simp'},
                                    headers={'Authorization': user_token})
        self.assertEqual(simp_info.json(), {'detail': 'This user has sent you a friend request'})

        noname_info = self.client.get(reverse('info'), {'username': 'noname'},
                                      headers={'Authorization': user_token})
        self.assertEqual(noname_info.json(), {'detail': 'You don\'t have any interactions with this user'})

    def test_request_cases(self):

        user_token, friend_token, requested_token, simp_token, noname_token = self.preparation()

        self.client.post(reverse('requests_send'), data={'to_user': 'user'}, headers={'Authorization': requested_token})
        self.client.post(reverse('requests_send'), data={'to_user': 'user'}, headers={'Authorization': friend_token})
        self.client.post(reverse('requests_send'), data={'to_user': 'user'}, headers={'Authorization': simp_token})
        self.client.post(reverse('requests_send'), data={'to_user': 'user'}, headers={'Authorization': noname_token})

        requests_list = self.client.get(reverse('requests'), headers={'Authorization': user_token})
        self.assertEqual(requests_list.json(), [
            {'from_user': 'requested', 'to_user': 'user', 'status': 'has been sent'},
            {'from_user': 'friend', 'to_user': 'user', 'status': 'has been sent'},
            {'from_user': 'simp', 'to_user': 'user', 'status': 'has been sent'},
            {'from_user': 'noname', 'to_user': 'user', 'status': 'has been sent'}
        ])

        self.client.post(reverse('requests_manage'), data={
            'request_sender': 'simp', 'decision': False
        }, headers={'Authorization': user_token})
        self.client.post(reverse('requests_manage'), data={
            'request_sender': 'friend', 'decision': True
        }, headers={'Authorization': user_token})
        self.client.post(reverse('requests_manage'), data={
            'request_sender': 'requested', 'decision': True
        }, headers={'Authorization': user_token})

        friend_list = self.client.get(reverse('friends'), headers={'Authorization': user_token})
        self.assertEqual(friend_list.json(), [{'friend': 'friend'}, {'friend': 'requested'}])

        self.client.delete(reverse('requests_delete'), data={
            'from_user': 'noname'
        }, headers={'Authorization': user_token})

        requests_list_last = self.client.get(reverse('requests'), headers={'Authorization': user_token})
        self.assertEqual(requests_list_last.json(), [
            {'from_user': 'simp', 'to_user': 'user', 'status': 'rejected by receiver'}
        ])

