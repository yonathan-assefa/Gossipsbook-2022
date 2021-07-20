# Generated by Django 3.2.4 on 2021-07-10 10:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0025_friendrequest_accepted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='circle',
            name='followers',
            field=models.ManyToManyField(related_name='user_circle_followers', through='users.CircleFollower', to=settings.AUTH_USER_MODEL),
        ),
    ]