from django.contrib.auth.models import User
from django.db import transaction
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# from mp_app.models import User


TEST_USERNAME = 'lucas'
TEST_EMAIL = 'lucas@gmail.com'
TEST_PASSWORD = 'abc123'


class TestSignUp(APITestCase):

    def create_user(self, is_seller=False):
        with transaction.atomic():
            url = reverse('sign-up')
            data = {
                'username': TEST_USERNAME,
                'email': TEST_EMAIL,
                'password': TEST_PASSWORD,
                'is_seller': is_seller
            }

            return self.client.post(url, data, format='json')

    def test_sign_up_as_buyer(self):
        response = self.create_user()

        db_user = User.objects.get()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(db_user.username, TEST_USERNAME)
        self.assertEqual(db_user.buyer.count(), 1)
        self.assertEqual(db_user.seller.count(), 0)


    def test_sign_up_as_seller(self):
        response = self.create_user(is_seller=True)

        db_user = User.objects.get()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(db_user.username, TEST_USERNAME)
        self.assertEqual(db_user.buyer.count(), 0)
        self.assertEqual(db_user.seller.count(), 1)


    def test_create_user_twice(self):
        response1 = self.create_user()
        response2 = self.create_user()

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        
        self.assertEqual(
            User.objects.filter(username=TEST_USERNAME).count(),
            1  
        )