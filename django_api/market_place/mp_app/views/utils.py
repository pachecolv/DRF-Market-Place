from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

from mp_app.models import Buyer
from mp_app.models import Seller

def get_buyer(request):
    try:
        return request.user.buyer.get()
    except Buyer.DoesNotExist:
        raise PermissionDenied(detail='User must be a buyer')

def get_seller(request):
    try:
        return request.user.seller.get()
    except Seller.DoesNotExist:
        raise PermissionDenied(detail='User must be a seller')
