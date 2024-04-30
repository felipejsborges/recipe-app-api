from core.models import Recipe
from recipes.serializers import RecipeDetailSerializer, RecipeImageSerializer, RecipesSerializer
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class RecipesViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        if self.action == "list":
            return RecipesSerializer

        if self.action == "upload_image":
            return RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=["PATCH"], detail=True, url_path="upload-image")
    def upload_image(self, *args, **kwargs):  # pylint: disable=unused-argument
        recipe = self.get_object()

        serializer = self.get_serializer(recipe, data=self.request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
