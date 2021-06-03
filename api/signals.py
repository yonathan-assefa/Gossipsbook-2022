from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.core.mail import send_mail
from django_rest_passwordreset.signals import reset_password_token_created


# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
#     email_message = f"{reverse('password_reset:reset-password-request')}?token={reset_password_token.key}"
#     title = "GossipsBook"
#     print("TOken Generating...")
#     send_mail(
#         # title:
#         f"Password Reset For {title}.",
#         # Message: 
#         email_message,
#         # from:
#         "gossipsbook.in@gmail.com",
#         # to
#         [reset_password_token.user.email, ]
#     )
