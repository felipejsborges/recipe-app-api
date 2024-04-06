from rest_framework import generics
from users.serializers import UsersSerializer


class UserIndexView(generics.CreateAPIView):
    serializer_class = UsersSerializer
