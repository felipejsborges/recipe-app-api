"""
Basic docs: https://django-filter.readthedocs.io/en/latest/guide/usage.html
Advanced docs: https://django-filter.readthedocs.io/en/latest/ref/filters.html
"""

from core.models import Recipe
from django_filters import rest_framework as filters


class RecipeFilter(filters.FilterSet):
    tags = filters.CharFilter(method="_filter_in")
    ingredients = filters.CharFilter(method="_filter_in")
    title = filters.CharFilter(lookup_expr="iexact")
    price_gte = filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_lte = filters.NumberFilter(field_name="price", lookup_expr="lte")
    time_to_make_in_minutes_gte = filters.NumberFilter(field_name="time_to_make_in_minutes", lookup_expr="gte")
    time_to_make_in_minutes_lte = filters.NumberFilter(field_name="time_to_make_in_minutes", lookup_expr="lte")

    class Meta:
        model = Recipe
        fields = ["time_to_make_in_minutes", "price"]

    def _filter_in(self, queryset, name, value):
        return queryset.filter(**{f"{name}__in": value.split(",")})
