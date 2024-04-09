from rest_framework import authentication, generics, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.settings import api_settings
from users.serializers import AuthTokenSerializer, UsersSerializer


class UsersIndexView(generics.CreateAPIView):
    serializer_class = UsersSerializer


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UsersDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UsersSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def patch(self, *args, **kwargs):  # pylint: disable=unused-argument
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
