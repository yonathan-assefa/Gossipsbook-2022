from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from PIL import Image
from string import ascii_letters
from random import choice


def upload_location(instance, filename, *args, **kwargs):
    file_path = 'profile/{author_id}/{filename}'.format(author_id=str(instance.user.id), filename=filename)
    return file_path


def create_random_slug(number=10):
    return "".join(choice(ascii_letters) for i in range(number))


class Interests(models.Model):
    title = models.CharField(max_length=75, unique=True)
    description = models.TextField(max_length=300, blank=True, null=True, 
               help_text='You can optionally provide a description for this interest')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Interests'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_location, blank=True, null=True)
    bio = models.TextField(max_length=455, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    designation = models.CharField(max_length=255, null=True, blank=True)
    languages = models.CharField(max_length=255, null=True, blank=True)
    interests = models.ManyToManyField(Interests, related_name='interests', blank=True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    following = models.ManyToManyField(User, related_name='following', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} profile"

    # reduce the size of the image if it's more than 1000px
    def save(self, *args, **kwargs):
        super().save( *args, **kwargs)
        
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 1000 or img.width > 1000:
                output = (600, 600)
                img.thumbnail(output)
                img.save(self.image.path)

def user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(user_profile, sender=User)

@receiver(post_delete, sender=Profile)
def delete_image(sender, instance, *args, **kwargs):
    instance.image.delete(False)


class WorkExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="work_experiences")
    company_name = models.CharField(max_length=250)
    company_post = models.CharField(max_length=250)
    text = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} Work-Experience..."


class Qualification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="qualifications")
    link = models.CharField(max_length=5000)    
    text = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} Qualification..."


class Circle(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="circle")
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} |-Circle"

    def save(self, *args, **kwargs):
        slug = self.slug
        if (slug is None) or (slug == "") or (slug == "slug"):
            self.slug = slugify(str(self.title[:8]) + create_random_slug(number=12))

        return super().save(*args, **kwargs)


class CircleInfo(models.Model):
    CATEGORY = (
        ("CB", "CELEBRITIES"),
        ("CY", "COMPANY"),
        ("IF", "INFLUENCERS"),
        ("EP", "ENTREPRENEURS"),
    )
    circle = models.OneToOneField(Circle, on_delete=models.CASCADE, related_name="info")
    description = models.TextField(null=True)
    category = models.CharField(max_length=2, choices=CATEGORY, null=True)
    verified = models.BooleanField(default=False)
    bio = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.circle.title + "| Info"


class CirclePhoto(models.Model):
    circle = models.OneToOneField(Circle, on_delete=models.CASCADE, related_name="picture")
    profile_pic = models.ImageField(upload_to="circle/profile-pic")
    cover_pic = models.ImageField(upload_to="circle/cover-pic")
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.circle.title + " |Photo"
