from rest_framework import serializers

class SignUpSerializer(serializers.ModelSerializer):
	username = serializers.CharField(max_length=200)
	email = serializers.EmailField()
	password = serializers.CharField(max_length=200)
	is_seller = serializers.BooleanField(default=False)

	


		