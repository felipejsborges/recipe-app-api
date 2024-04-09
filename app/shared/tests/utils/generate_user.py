from django.contrib.auth import get_user_model


def generate_sample_user_payload(**params):
    return {"email": "test@example.com", "password": "test_pass_123", "name": "Test Name", **params}


def generate_sample_user(**params):
    return get_user_model().objects.create_user(**{**generate_sample_user_payload(), **params})
