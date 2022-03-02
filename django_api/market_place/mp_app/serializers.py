from rest_framework import serializers

from .models import Product
from .models import Seller
from .models import Transaction
from .models import WishList

class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=200, write_only=True)
    is_seller = serializers.BooleanField(default=False)


class SellerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Seller
        exclude = ['user']
        read_only_fields = ['created_at']

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.display_name = validated_data.get('display_name', instance.display_name)
        instance.save()

        return instance

class ProductSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.display_name', read_only=True)

    class Meta:
        model = Product
        exclude = ['seller']

class BuyProductSerialzer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=0)
    qty = serializers.IntegerField(min_value=0)

class TransactionSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Transaction
        exclude = ['id', 'buyer']
        read_only_fields = [
            'product', 'unity_price', 
            'total_amount', 'timestamp',
            'product_id', 'product_name'
        ]

    def create(self, validated_data):
        unity_price = validated_data['product'].price
        total_amount = validated_data['qty'] * unity_price

        return Transaction(
            buyer=validated_data['buyer'],
            product=validated_data['product'],
            qty=validated_data['qty'],
            unity_price=unity_price,
            total_amount=total_amount 
        )


class WishListSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_description = serializers.CharField(source='product.description', read_only=True)
    product_price = serializers.FloatField(source='product.price', read_only=True)

    class Meta:
        model = WishList
        fields = ['product_id', 'product_name', 'product_description', 'product_price']

    def create(self, validated_data):
        print('got here')
        print(validated_data['buyer'])

        return WishList.objects.create(
            buyer=validated_data['buyer'],
            product=validated_data['product']
        )