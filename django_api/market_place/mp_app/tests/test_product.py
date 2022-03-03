from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from mp_app.models import Product
from mp_app.models import Seller
from mp_app.tests.common import create_user


class TestCreateProduct(APITestCase):

    def setUp(self):
        self.user = create_user('user1', '123')
        self.seller = Seller.objects.create(user=self.user)

    def test_create_product(self):
        # Check prouduct is not on database yet
        self.assertFalse(
            Product.objects.filter(seller=self.seller, name='product 1').exists()
        )

        url = reverse('products-list')
        self.client.force_authenticate(user=self.user)
        payload = {
            'name': 'product 1',
            'description': 'description product 1',
            'price': 100,
            'qty_available': 10,
            'max_qty_customer': 2
        }

        response = self.client.post(url, payload, format='json')

        # Test product was created in the database
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Product.objects.filter(seller=self.seller, name='product 1').exists()
        )

    def test_create_product_missing_price(self):
        url = reverse('products-list')
        self.client.force_authenticate(user=self.user)
        payload = {
            'name': 'product 1',
            'description': 'description product 1',
            'qty_available': 10,
            'max_qty_customer': 2
        }
        
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ProductDetail(APITestCase):

    def setUp(self):
        self.user_1 = create_user('user1', '123')
        self.user_2 = create_user('user2', '123')
        self.seller_1 = Seller.objects.create(user=self.user_1)
        self.seller_2 = Seller.objects.create(user=self.user_2)

        self.product = Product.objects.create(
            name='Product 1',
            price=10,
            seller=self.seller_1
        )

    def test_update_price(self):
        url = reverse('product-detail', args=[self.product.id])
        payload = {'price': 15}

        self.client.force_authenticate(user=self.user_1)
        response = self.client.put(url, payload, format='json')

        self.product.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.product.price, 15)

    def test_update_wrong_seller(self):
        url = reverse('product-detail', args=[self.product.id])
        payload = {'price': 15}

        self.client.force_authenticate(user=self.user_2)
        response = self.client.put(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)