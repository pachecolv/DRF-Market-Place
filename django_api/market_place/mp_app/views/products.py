from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from mp_app.models import Product 
from mp_app.serializers import ProductSerializer


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
        serializer = ProductSerializer(product, request.data, partial=True)
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