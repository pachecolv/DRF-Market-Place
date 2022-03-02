
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from mp_app.models import Product
from mp_app.models import SellerBalance
from mp_app.serializers import TransactionSerializer
from .utils import get_buyer

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
        buyer = get_buyer(request)

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
