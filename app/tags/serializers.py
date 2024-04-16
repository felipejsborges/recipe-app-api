from core.models import Tag
from rest_framework import serializers


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]
