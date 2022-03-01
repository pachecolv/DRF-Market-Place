from rest_framework import serializers

class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=200, write_only=True)
    is_seller = serializers.BooleanField(default=False)


        