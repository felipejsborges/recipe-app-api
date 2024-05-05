from django_filters import rest_framework as filters


class IsOwnerFilterBackend(filters.DjangoFilterBackend):
    def filter_queryset(self, request, queryset, _):
        return queryset.filter(user=request.user)
