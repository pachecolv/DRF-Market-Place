from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status

from .utils import get_seller
from mp_app.models import Product
from mp_app.serializers import SellerSerializer
from mp_app.serializers import ProductSerializer

class SellerDetail(APIView):

    def get(self, request, format=None):
        seller = get_seller(request)
        serializer = SellerSerializer(seller)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        seller = get_seller(request)

        serializer = SellerSerializer(seller, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data)

class SellerProducts(APIView):

    def get(self, request, format=None):
        seller = get_seller(request)
        products = Product.objects.filter(seller=seller)
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)