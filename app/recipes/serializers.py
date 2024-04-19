from core.models import Recipe
from ingredients.serializers import IngredientsSerializer
from rest_framework import serializers
from shared.utils.get_or_create_ingredients_for_recipe import get_or_create_ingredients_for_recipe
from shared.utils.get_or_create_tags_for_recipe import get_or_create_tags_for_recipe
from tags.serializers import TagsSerializer


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True, required=False)
    ingredients = IngredientsSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ["id", "title", "time_to_make_in_minutes", "price", "link", "tags", "ingredients"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        tags = self._pop_tags(validated_data)
        ingredients = self._pop_ingredients(validated_data)
        instance = self._create_instance(validated_data)
        get_or_create_tags_for_recipe(instance, tags)
        get_or_create_ingredients_for_recipe(instance, ingredients)

        return instance

    def update(self, instance, validated_data):
        self._update_tags(instance, validated_data)
        self._update_ingredients(instance, validated_data)
        self._update_instance(instance, validated_data)

        return instance

    def _pop_tags(self, validated_data):
        return validated_data.pop("tags", [])

    def _pop_ingredients(self, validated_data):
        return validated_data.pop("ingredients", [])

    def _create_instance(self, validated_data):
        return Recipe.objects.create(**validated_data)

    def _update_tags(self, instance, validated_data):
        tags = validated_data.pop("tags", None)

        if tags is not None:
            instance.tags.clear()
            get_or_create_tags_for_recipe(instance, tags)

    def _update_ingredients(self, instance, validated_data):
        ingredients = validated_data.pop("ingredients", None)

        if ingredients is not None:
            instance.ingredients.clear()
            get_or_create_ingredients_for_recipe(instance, ingredients)

    def _update_instance(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()


class RecipeDetailSerializer(RecipesSerializer):

    class Meta(RecipesSerializer.Meta):
        fields = RecipesSerializer.Meta.fields + ["description"]
