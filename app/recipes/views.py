from core.models import Recipe
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema, extend_schema_view
from recipes.filters import RecipeFilter
from recipes.serializers import RecipeDetailSerializer, RecipeImageSerializer, RecipesSerializer
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

SEARCH_FIELDS = ["title", "description", "user__name", "user__email", "tags__name", "ingredients__name"]


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                "search",
                OpenApiTypes.STR,
                description="Search by: " + ", ".join(SEARCH_FIELDS),
            ),
        ]
    )
)
class RecipesViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_class = RecipeFilter
    search_fields = SEARCH_FIELDS

    def get_queryset(self):
        return self.queryset.order_by("-id").distinct()

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
