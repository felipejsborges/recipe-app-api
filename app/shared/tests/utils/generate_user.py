from django.contrib.auth import get_user_model


def generate_sample_user_payload(**params):
    user_quantity = get_user_model().objects.count()

    name = f"Test Name {user_quantity}"
    email = f"test{user_quantity}@email.com"

    return {"email": email, "password": "test_pass_123", "name": name, **params}


def generate_sample_user(**params):
    return get_user_model().objects.create_user(**{**generate_sample_user_payload(), **params})
