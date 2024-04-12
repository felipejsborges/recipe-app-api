from django.urls import include, path
from recipes import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", views.RecipesViewSet)

app_name = "recipes"  # pylint: disable=invalid-name

urlpatterns = [
    path("", include(router.urls)),
]
