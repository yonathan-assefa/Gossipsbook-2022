from django.contrib.auth.models import User
from django.db import models
from PIL import Image
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify

from answers.models import AnswersModel


def upload_location(instance, filename, *args, **kwargs):
    file_path = 'questions/{author_id}/{filename}'.format(author_id=str(instance.author.id), filename=filename)
    return file_path


class Tags(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=300, blank=True, null=True, help_text='You can optionally provide a '
                                                                                    'description for this tag')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Tags'


class QuestionsModel(models.Model):
    title = models.CharField(max_length=75, unique=True, help_text='What is the title of your question?',
                             verbose_name='Title')
    slug = models.SlugField(max_length=255, unique=True)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name='Date Published')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Date Updated')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_author')
    image = models.ImageField(upload_to=upload_location, blank=True, null=True, help_text='Add image (optional)')
    tags = models.ManyToManyField(Tags, name='q_tags', blank=True)
    vote_up = models.ManyToManyField(User, related_name='vote_up', blank=True)
    vote_down = models.ManyToManyField(User, related_name='vote_down', blank=True)
    shares = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('questions:question_detail', kwargs={'question_slug': self.slug})

    def get_delete_url(self):
        return reverse('questions:question_delete', kwargs={'question_slug': self.slug})

    def get_update_url(self):
        return reverse('questions:question_update', kwargs={'question_slug': self.slug})

    def get_answers(self):
        answers = AnswersModel.objects.filter(question=self)
        return answers

    def get_oppose_count(self):
        result = self.vote_down.all().count()
        return result

    def __str__(self):
        return self.title
    
    # reduce the size of the image if it's more than 1200px
    def save(self, *args, **kwargs):
        super().save( *args, **kwargs)
    
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 500 or img.width > 1000:
                output = (500, 1200)
                img.thumbnail(output)
                img.save(self.image.path)

    class Meta:
        verbose_name_plural = 'Questions'


@receiver(post_delete, sender=QuestionsModel)
def delete_image(sender, instance, *args, **kwargs):
    instance.image.delete(False)


def save_question_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


pre_save.connect(save_question_slug, sender=QuestionsModel)


def save_tag_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


pre_save.connect(save_tag_slug, sender=Tags)
