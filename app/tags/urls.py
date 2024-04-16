from django.urls import include, path
from rest_framework.routers import DefaultRouter
from tags import views

router = DefaultRouter()
router.register("", views.TagsViewSet)

app_name = "tags"  # pylint: disable=invalid-name

urlpatterns = [
    path("", include(router.urls)),
]
