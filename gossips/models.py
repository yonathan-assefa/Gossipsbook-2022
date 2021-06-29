from django.contrib.auth.models import User
from django.db import models
from PIL import Image
from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from random import choice
from users.models import Circle
from answers.models import AnswersModel
from django.http import Http404

def random_number_gen(number=4):
    return "".join(str(choice(range(9))) for i in range(number))


def upload_location(instance, filename, *args, **kwargs):
    file_path = 'gossips/{author_id}/{filename}'.format(author_id=str(instance.author.id), filename=filename)
    return file_path


class Tags(models.Model):
    title = models.CharField(max_length=55, unique=True)
    description = models.TextField(max_length=300, blank=True, null=True, help_text='You can optionally provide a '
                                                                                    'description for this tag')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Tags'

class GossipsModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gossip_author', null=True, blank=True)
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name="circle_gossips", null=True, blank=True)
    title = models.CharField(max_length=75, unique=True, help_text='What is the title of your gossip?',
                             verbose_name='Title')
    content = models.TextField(max_length=3000)
    slug = models.SlugField(max_length=255, unique=True)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name='Date Published')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Date Updated')
    image = models.ImageField(upload_to=upload_location, blank=True, null=True, help_text='Add image (optional)')
    tags = models.ManyToManyField(Tags, name='q_tags', blank=True)
    shares = models.IntegerField(default=0)
    true = models.ManyToManyField(User, blank=True, related_name="true")
    false = models.ManyToManyField(User, blank=True, related_name="false")
    link = models.CharField(max_length=2040, blank=True, null=True)  # 2040 is the maximum length for a link...
    from_question_user = models.CharField(max_length=255, blank=True, null=True)
    from_question_answer_provider = models.CharField(max_length=255, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('gossips:gossip_detail', kwargs={'gossip_slug': self.slug})

    def get_delete_url(self):
        return reverse('gossips:gossip_delete', kwargs={'gossip_slug': self.slug})

    def get_update_url(self):
        return reverse('gossips:gossip_update', kwargs={'gossip_slug': self.slug})
    
    def get_total_comments(self):
        return self.comments_set.all().order_by('-date_published')

    @property
    def percent_true(self):
        true_number = int(self.true.all().count())
        false_number = int(self.false.all().count())
        total_number = true_number + false_number

        try:
            calculate = (true_number / total_number) * 100
        except ZeroDivisionError:
            calculate = 0
        return calculate

    @property
    def percent_false(self):
        true_number = int(self.true.all().count())
        false_number = int(self.false.all().count())
        total_number = true_number + false_number
        try:
            calculate = (false_number / total_number) * 100
        except ZeroDivisionError:
            calculate = 0
        return calculate

    def get_total_voters(self):
        true_number = int(self.true.all().count())
        false_number = int(self.false.all().count())
        total_voters = true_number + false_number
        return total_voters

    def __str__(self):
        return self.title
    
    # reduce the size of the image if it's more than 1200px
    def save(self, *args, **kwargs):
        author = self.author
        circle = self.circle

        if (not author) and (not circle):
            raise Http404

        super().save( *args, **kwargs)
    
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 500 or img.width > 1000:
                output = (500, 1200)
                img.thumbnail(output)
                img.save(self.image.path)

    class Meta:
        verbose_name_plural = 'Gossips'


class Comments(models.Model):
    gossip = models.ForeignKey(GossipsModel, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    date_published = models.DateTimeField(auto_now_add=True, verbose_name='Date Published')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Date Updated')

    def __str__(self):
        return f"{self.author}'s comment on {self.gossip}"

    class Meta:
        verbose_name_plural = 'Comments'


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, related_name="replies")
    content = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


# signal that creates and saves gossips slug upon creation of a gossip
def save_gossip_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title) + "-" + str(random_number_gen())

pre_save.connect(save_gossip_slug, sender=GossipsModel)


