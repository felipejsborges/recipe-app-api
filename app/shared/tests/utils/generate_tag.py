from core.models import Tag
from django.conf import settings


def generate_sample_tag_payload(user: settings.AUTH_USER_MODEL, **params):
    defaults = {
        "user": user,
    }

    if "name" not in params:
        tag_quantity = Tag.objects.count()
        defaults["name"] = f"Sample Tag {tag_quantity}"

    defaults.update(params)

    return defaults


def generate_sample_tag(user: settings.AUTH_USER_MODEL, **params):
    payload = generate_sample_tag_payload(user, **params)

    return Tag.objects.create(**payload)
