# Generated by Django 3.0.8 on 2021-03-10 23:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import questions.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, help_text='You can optionally provide a description for this tag', max_length=300, null=True)),
            ],
            options={
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='QuestionsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='What is the title of your question?', max_length=75, unique=True, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('date_published', models.DateTimeField(auto_now_add=True, verbose_name='Date Published')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date Updated')),
                ('image', models.ImageField(blank=True, help_text='Add image (optional)', null=True, upload_to=questions.models.upload_location)),
                ('shares', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_author', to=settings.AUTH_USER_MODEL)),
                ('q_tags', models.ManyToManyField(blank=True, to='questions.Tags')),
                ('vote_down', models.ManyToManyField(blank=True, related_name='vote_down', to=settings.AUTH_USER_MODEL)),
                ('vote_up', models.ManyToManyField(blank=True, related_name='vote_up', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Questions',
            },
        ),
    ]
