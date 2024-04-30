from core.models import Recipe
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema, extend_schema_view
from recipes.serializers import RecipeDetailSerializer, RecipeImageSerializer, RecipesSerializer
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from shared.views import transform_strings_into_list_of_integers


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                "tags",
                OpenApiTypes.STR,
                description="Comma separated list of tag IDs to filter the recipes",
            ),
            OpenApiParameter(
                "ingredients",
                OpenApiTypes.STR,
                description="Comma separated list of ingredient IDs to filter the recipes",
            ),
        ]
    )
)
class RecipesViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        self._filter_queryset_by_tags()
        self._filter_queryset_by_ingredients()

        return self.queryset.filter(user=self.request.user).order_by("-id").distinct()

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

    def _filter_queryset_by_tags(self):
        tags = self.request.query_params.get("tags")

        if not tags:
            return

        tag_ids = transform_strings_into_list_of_integers(tags)
        self.queryset = self.queryset.filter(tags__id__in=tag_ids)

    def _filter_queryset_by_ingredients(self):
        ingredients = self.request.query_params.get("ingredients")

        if not ingredients:
            return

        ingredient_ids = transform_strings_into_list_of_integers(ingredients)
        self.queryset = self.queryset.filter(ingredients__id__in=ingredient_ids)
