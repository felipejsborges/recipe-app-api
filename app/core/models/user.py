from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django_rest_passwordreset.models import ResetPasswordToken


def generate_token_for_user(user: settings.AUTH_USER_MODEL):
    # if not user.eligible_for_reset():
    #     raise ValueError("User is not eligible for password reset.")
    password_reset_tokens = user.password_reset_tokens.all()

    if password_reset_tokens.exists():
        return password_reset_tokens.first()

    return ResetPasswordToken.objects.create(user=user)


def send_email_to_register_password(token):
    context = {"token": token}

    template_name = "emails/password_registration.html"
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject="Password Registration",
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

        token = generate_token_for_user(user)
        send_email_to_register_password(token.key)

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
