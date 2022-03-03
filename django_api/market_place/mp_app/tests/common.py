from django.contrib.auth.models import User


def create_user(username, password):
    return User.objects.create_user(username=username, password=password)