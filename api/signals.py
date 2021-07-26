from api.models import RestToken
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.core.mail import send_mail
from django_rest_passwordreset.signals import reset_password_token_created
from users.models import Circle, CircleInfo, CirclePhoto
from django.core.mail import send_mail


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

@receiver(signal=post_save, sender=Circle)
def create_circle_info(sender, instance, created, **kwargs):
    if created:
        obj = CircleInfo.objects.create(circle=instance)
        return obj


@receiver(signal=post_save, sender=Circle)
def create_circle_photo(sender, instance, created, **kwargs):
    if created:
        obj = CirclePhoto.objects.create(circle=instance)
        return obj


@receiver(signal=post_save, sender=RestToken)
def send_mail(sender, instance, created, **kwargs):
    if created:
        email = "suhaibsafwan45@gmail.com"
        print("Sending a Mail to " + email)
        send_mail(
            subject="Sending a Mail",
            message=f"Rest Token is from Signal that is {instance.token}", 
            from_email="gossipsbook.in@gmail.com",
            recipient_list=[email, ],
            fail_silently=False
        )

