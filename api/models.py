from django.db import models
from django.utils import timezone
from random import choice
from string import ascii_letters
from django.contrib.auth.models import User
from django.core.mail import send_mail


def create_token(number=8):
    return "".join(choice(ascii_letters) for i in range(number))


class RestToken(models.Model):
    """
    This Token is being generated when User Forgots His Password...
    """
    token = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    expired = models.BooleanField(default=False)

    def is_token_valid(self):
        date = self.date_created
        time_dl = timezone.now() - date
        if time_dl.days >= 1:
            return False

        return True

    def save(self, *args, **kwargs):
        new_token = create_token()
        user_email = self.user.email

        print("Inside Models -> ", user_email)
        
        if not self.token:
            self.token = new_token

        return super().save(*args, **kwargs)