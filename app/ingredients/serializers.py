from core.models import Ingredient
from rest_framework import serializers


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name"]
        read_only_fields = ["id"]
