from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from mp_app.models import Buyer
from mp_app.models import Product
from mp_app.models import Seller
from mp_app.models import SellerBalance
from mp_app.tests.common import create_user

class TestBuyProduct(APITestCase):

    def setUp(self):
        self.user_1 = create_user('user_1', '123')
        self.user_2 = create_user('user_2', '123')

        self.seller = Seller.objects.create(user=self.user_1)
        self.buyer = Buyer.objects.create(user=self.user_2)

        self.product = Product.objects.create(
            seller=self.seller,
            name='product 1',
            price=10,
            qty_available=10,
            max_qty_customer=5,
        )


    def get_seller_balance(self, seller):
        seller_balance_obj = SellerBalance.objects.filter(seller=seller)\
            .order_by('timestamp')\
            .last()

        if not seller_balance_obj:
            return 0

        return seller_balance_obj.balance

    def test_purchase(self):
        qty_1 = 3
        product_initial_qty = self.product.qty_available
        initial_seller_balance = self.get_seller_balance(self.seller)

        # Make a purchase
        url = reverse('buy-product', args=[self.product.id])
        payload = {'qty': qty_1}
        self.client.force_authenticate(user=self.user_2)
        response = self.client.post(url, payload)

        # Verify db after purchase
        self.product.refresh_from_db()
        self.assertEqual(
            self.product.qty_available,
            product_initial_qty - qty_1
        )
        new_balance = self.get_seller_balance(self.seller)
        self.assertEqual(
            new_balance,
            initial_seller_balance + qty_1 * self.product.price
        )

        # Make another purchase
        product_qty = self.product.qty_available
        seller_balance = new_balance

        qty_2 = 2
        payload = {'qty': qty_2}
        response = self.client.post(url, payload)

        self.product.refresh_from_db()
        self.assertEqual(
            self.product.qty_available,
            product_qty - qty_2
        )

        new_balance = self.get_seller_balance(self.seller)
        self.assertEqual(
            new_balance,
            seller_balance + qty_2 * self.product.price
        )