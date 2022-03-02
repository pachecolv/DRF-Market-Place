from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import render
from django.db import transaction
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView 

from .models import Buyer, Seller, Product
from .models import SellerBalance
from .serializers import SignUpSerializer, ProductSerializer, SellerSerializer, TransactionSerializer


# Create your views here.

class SignUp(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = SignUpSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(
                serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
        except IntegrityError:
            return Response(
                'User already exists.',
                status=status.HTTP_400_BAD_REQUEST
            )

        if serializer.data['is_seller']:
            seller = Seller(user=user).save()
        else:
            buyer = Buyer(user=user).save()

        return Response(
            f'User {user.username} created.',
            status=status.HTTP_201_CREATED
        )


class SellerDetail(APIView):

    def get(self, request, format=None):
        seller = request.user.seller.get()
        serializer = SellerSerializer(seller)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        seller = request.user.seller.get()
        serializer = SellerSerializer(seller, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data)


class ProductsList(APIView):

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        seller = request.user.seller.get()

        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(seller=seller)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductDetail(APIView):

    def get(self, request, pk, format=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

        serializer = ProductSerializer(product)

        return Response(serializer.data)

    def put(self, request, pk, format=None):
        seller = request.user.seller.get()

        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

        product.delete()

        return Response(f'Product {pk} deleted.')

class BuyProduct(APIView):

    def update_seller_balance(self, seller, value_add):
        balance_row = SellerBalance.objects\
            .filter(seller=seller)\
            .order_by('-timestamp')\
            .last()

        if balance_row:
            new_balance = balance_row.balance + value_add
        else:
            new_balance = value_add

        return SellerBalance(seller=seller, balance=new_balance)


    def post(self, request, pk):
        buyer = request.user.buyer.get()
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

        # Check if request is valid
        serializer = TransactionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Check if there are enough products in stock
        if serializer.validated_data['qty'] > product.qty_available:
            return Response(
                f'There are only {product.qty_available} units available.',
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if qty is greater than max qty per customer
        if serializer.validated_data['qty'] > product.max_qty_customer:
            return Response(
                f'Max quantity allowed is {product.max_qty_customer}',
                status=status.HTTP_400_BAD_REQUEST
            )   

        # Move forward with transactions
        tx = serializer.save(buyer=buyer, product=product)
        product.qty_available -= tx.qty
        balance = self.update_seller_balance(product.seller, tx.total_amount)

        tx.save()
        product.save()
        balance.save()

        serializer = TransactionSerializer(tx)

        return Response(serializer.data)
