from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.

class SignUp(APIView):
	permission_classes = [AllowAny]

	def post(self, request, format=None):