from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.views import APIView 
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from mp_app.serializers import SignUpSerializer
from mp_app.models import Buyer
from mp_app.models import Seller

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
