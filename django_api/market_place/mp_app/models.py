from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

# Create your models here

class Buyer(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='buyer',
        on_delete=models.CASCADE
    )

class Seller(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='seller',
        on_delete=models.CASCADE
    )
    display_name = models.CharField(max_length=200, default='')
    created_at = models.DateTimeField(default=now)
    bio = models.TextField(null=True)     


class Product(models.Model):
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    qty_available = models.PositiveIntegerField(default=0)
    max_qty_customer = models.PositiveIntegerField(default=None, null=True)


class Transaction(models.Model):
    buyer = models.ForeignKey('Buyer', on_delete=models.CASCADE)
    product = models.ForeignKey(
        'Product',
        related_name='transaction',
        on_delete=models.CASCADE, 
    )
    qty = models.PositiveIntegerField()
    unity_price = models.FloatField()
    total_amount = models.FloatField()
    timestamp = models.DateTimeField(default=now)


class TransactionItem(models.Model):
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    unity_price = models.FloatField()


class SellerBalance(models.Model):
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE)
    balance = models.FloatField()
    timestamp = models.DateTimeField(default=now)


class WishList(models.Model):
    buyer = models.ForeignKey('Buyer', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=now)
