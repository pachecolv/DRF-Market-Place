from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status


from mp_app.serializers import SellerSerializer

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