from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView 

from mp_app.models import Product
from mp_app.models import WishList
from mp_app.serializers import WishListSerializer
from .utils import get_buyer

class WishListView(APIView):

    def get(self, request, format=None):
        buyer = get_buyer(request)
        items = WishList.objects.filter(buyer=buyer)
        serializer = WishListSerializer(items, many=True)

        return Response(serializer.data)
    

class WishListDetail(APIView):

    def post(self, request, pk, format=None):
        buyer = get_buyer(request)
        product = Product.objects.get(pk=pk) 

        serializer = WishListSerializer(data=request.data)
        serializer.is_valid()

        serializer.save(product=product, buyer=buyer)

        return Response(serializer.data)

    def delete(self, request, pk):
        buyer = get_buyer(request)
        try:
            list_item = WishList.objects.get(buyer=buyer, product__id=pk)
        except WishList.DoesNotExist:
            raise PermissionDenied(detail='Product is not in wish list')

        list_item.delete()

        return Response("Item deleted")