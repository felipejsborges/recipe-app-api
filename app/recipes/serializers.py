from core.models import Recipe
from rest_framework import serializers


class RecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ["id", "title", "time_to_make_in_minutes", "price", "link"]
        read_only_fields = ["id"]


class RecipeDetailSerializer(RecipesSerializer):

    class Meta(RecipesSerializer.Meta):
        fields = RecipesSerializer.Meta.fields + ["description"]
