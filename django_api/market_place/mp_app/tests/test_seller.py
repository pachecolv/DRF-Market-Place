from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from mp_app.models import Buyer
from mp_app.models import Product
from mp_app.models import Seller
from mp_app.tests.common import create_user


class TestSellerDetail(APITestCase):

    def setUp(self):
        self.user1 = create_user('seller1', '123')
        self.user2 = create_user('seller2', '123')
        self.user3 = create_user('buyer3', '123')

        self.seller1 = Seller.objects.create(
            user=self.user1,
            display_name='seller1 store',
            bio=''
        )
        self.seller2 = Seller.objects.create(
            user=self.user2,
            display_name='seller2 store',
            bio='the best store in town'
        )
        self.buyer3 = Buyer.objects.create(user=self.user3)

    def test_get_seller_detail(self):        
        # Check details for seller 1
        self.client.force_authenticate(user=self.user1)
        url = reverse('seller-detail')
        response = self.client.get(url)

        self.assertEqual(response.data['username'], 'seller1')
        self.assertEqual(response.data['display_name'], 'seller1 store')
        self.assertEqual(response.data['bio'], '')

        # Check details for seller 2
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(url)

        self.assertEqual(response.data['username'], self.seller2.user.username)
        self.assertEqual(response.data['display_name'], self.seller2.display_name)
        self.assertEqual(response.data['bio'], self.seller2.bio)

    def test_get_seller_detail_wrong_user(self):
        # Authenticate as a buyer
        self.client.force_authenticate(user=self.user3)
        url = reverse('seller-detail')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_seller_display_name(self):
        new_display_name = 'seller 1 mega store'
        url = reverse('seller-detail')
        payload = {'display_name': new_display_name}

        self.client.force_authenticate(user=self.user1)
        response = self.client.put(url, payload, format='json')

        # Check if display_name was updated
        self.seller1.refresh_from_db()
        self.assertEqual(self.seller1.display_name, new_display_name)

        # Check if seller 2 was not impacted
        self.seller2.refresh_from_db()
        self.assertEqual(self.seller2.display_name, 'seller2 store')

    def test_update_seller_bio(self):
        new_bio = 'This is the best store you can find!'
        url = reverse('seller-detail')
        payload = {'bio': new_bio}

        self.client.force_authenticate(user=self.user1)
        response = self.client.put(url, payload, format='json')

        self.seller1.refresh_from_db()
        self.assertEqual(self.seller1.bio, new_bio)

    def test_try_update_seller_as_buyer(self):
        url = reverse('seller-detail')
        payload = {'display_name': 'new_name'}

        response = self.client.put(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestSellerProducts(APITestCase):

    def setUp(self):
        self.user_1 = create_user('seller1', '123')
        self.user_2 = create_user('seller2', '123')

        self.seller_1 = Seller.objects.create(
            user=self.user_1,
            display_name='seller1 store',
            bio=''
        )
        self.seller_2 = Seller.objects.create(
            user=self.user_2,
            display_name='seller2 store',
            bio='the best store in town'
        )

        self.product_1 = Product.objects.create(
            seller=self.seller_1,
            name='product 1',
            price=10,
            qty_available=10,
            max_qty_customer=2
        )

        self.product_2 = Product.objects.create(
            seller=self.seller_1,
            name='product 2',
            price=20,
            qty_available=10,
            max_qty_customer=2
        )

        self.product_3 = Product.objects.create(
            seller=self.seller_2,
            name='product 3',
            price=30,
            qty_available=10,
            max_qty_customer=2
        )

    def test_get_seller_products(self):
        url = reverse('seller-products')
        self.client.force_authenticate(user=self.user_1)        
        response = self.client.get(url)

        self.assertEqual(len(response.data), 2)

        self.assertTrue(
            next((x for x in response.data if x['id'] == self.product_1.id), False)
        )
        self.assertTrue(
            next((x for x in response.data if x['id'] == self.product_2.id), False)
        )
        self.assertFalse(
            next((x for x in response.data if x['id'] == self.product_3.id), False)
        )

        print(response.data)