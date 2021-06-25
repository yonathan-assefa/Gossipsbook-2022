# Generated by Django 3.2.4 on 2021-06-23 06:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0016_circlefollower'),
    ]

    operations = [
        migrations.AddField(
            model_name='circle',
            name='followers',
            field=models.ManyToManyField(related_name='user_followers', through='users.CircleFollower', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='circlefollower',
            name='circle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower_set', to='users.circle'),
        ),
    ]