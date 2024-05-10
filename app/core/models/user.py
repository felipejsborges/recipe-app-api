from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email_to_user():
    context = {
        "receiver_name": "Klayton Claudio",
        "age": 24,
        "profession": "Software Dev",
        "marital_status": "Married",
        "address": "Jamil e uma noites",
        "year": 2024,
    }

    template_name = "emails/tmp.html"
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject="Salve",
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=["felipejsborges13@gmail.com"],
        # bcc=["felipejsborges@outlook.com"],
        # reply_to=["another@example.com"],
        # headers={"Message-ID": "foo"},
    )
    email.attach_alternative(html_content, "text/html")

    email.send(fail_silently=False)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        send_email_to_user()

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
