from django.urls import include, path
from ingredients import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", views.IngredientsViewSet)

app_name = "ingredients"  # pylint: disable=invalid-name

urlpatterns = [
    path("", include(router.urls)),
]
