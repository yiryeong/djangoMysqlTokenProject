# import json
# from django.urls import include, path, reverse
# from rest_framework import status
# from rest_framework.test import APITestCase, URLPatternsTestCase
# from payhistory.models import User, PayHistory
#
#
# class UserTest(APITestCase, URLPatternsTestCase):
#     """ Test module for User """
#
#     urlpatterns = [
#         path('api/', include('payhistory.urls')),
#     ]
#
#     data = {
#         'email': 'test@test.com',
#         'password': 'test'
#     }
#
#     def setUp(self):
#         # create User Infos
#         User.objects.create(email=self.data['email'], password=self.data['password'])
#         User.objects.create(email='test1@test.com', password='test1')
#
#         # create Pay History Data
#         PayHistory.objects.create(datetime="2021-11-01 13:14:15", price=100, memo="record1", uid=1)
#         pass
#
#     def test_login(self):
#         """ Test if a user can login and get a JWT response token """
#         url = reverse('login')
#         response = self.client.post(url, self.data)
#         response_data = json.loads(response.content)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue('access' in response_data)
#
#     def test_user_registration(self):
#         """ Test if a user can register """
#         url = reverse('register')
#         data = {
#             'email': 'test2@test.com',
#             'password': 'test2',
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
