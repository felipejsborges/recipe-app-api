from django.urls import path
from users import views

app_name = "users"  # pylint: disable=invalid-name

urlpatterns = [
    path("", views.UserIndexView.as_view(), name="index"),
]
