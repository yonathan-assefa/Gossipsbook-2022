from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.db import models
from django.http import Http404
from gossips.models import GossipsModel, random_number_gen
from cheaters.models import CheatersModel
from django.utils.text import slugify


class FalseInformation(models.Model):
   gossip = models.ForeignKey(GossipsModel, on_delete=models.CASCADE, related_name='false_gossip', null=True, blank=True)
   section = models.CharField(max_length=255)
   date_published = models.DateTimeField(auto_now_add=True, verbose_name='Date Published')
   date_updated = models.DateTimeField(auto_now=True, verbose_name='Date Updated')

   def __str__(self):
      return f"{self.gossip}"
    

# signal that calculates whether a gossip should be added to false information section or not
def gossip_false_information(sender, instance, *args, **kwargs):
   total_votes = instance.true.all().count() + instance.false.all().count()
   if total_votes >= 100:
      percent_false = instance.percent_false
      if int(percent_false) >= 51:
         if not FalseInformation.objects.filter(gossip__title=instance.title).exists():
            FalseInformation.objects.create(gossip=instance, section='gossip')
      else:
         if FalseInformation.objects.filter(gossip__title=instance.title).exists():
            FalseInformation.objects.get(gossip__title=instance.title).delete()
   else:
      print('NEGATIVE')

post_save.connect(gossip_false_information, sender=GossipsModel)


# signal that calculates whether a cheater should be added to false information section or not
def cheater_false_information(sender, instance, *args, **kwargs):
   total_votes = instance.true.all().count() + instance.false.all().count()
   if total_votes >= 100:
      percent_false = instance.percent_false
      if int(percent_false) >= 51:
         if not FalseInformation.objects.filter(cheater__title=instance.title).exists():
            FalseInformation.objects.create(cheater=instance, section='cheater')
      else:
         if FalseInformation.objects.filter(cheater__title=instance.title).exists():
            FalseInformation.objects.get(cheater__title=instance.title).delete()
   else:
      print('NEGATIVE')

post_save.connect(cheater_false_information, sender=CheatersModel)



class RFRModel(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
   gossip = models.ForeignKey(GossipsModel, on_delete=models.SET_NULL, null=True)
   reason = models.TextField(max_length=955)
   section = models.CharField(max_length=255)
   date_submitted = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return self.reason

   class Meta:
      unique_together = ["user", "gossip"]


class FeedbackModel(models.Model):
   user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # because non logged in users can give feedback
   email = models.EmailField(null=True) # because non logged in users can give feedback
   slug = models.SlugField()
   message = models.CharField(max_length=955)
   date_submitted = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return self.message

   def save(self, *args, **kwargs):
      user = self.user
      email = self.email
      if (not user) and (not email):
         raise Http404("Please Provide an Email or be Authenticated...")

      slug = self.slug
      if (slug is None) or (slug == ""):
         self.slug = slugify(self.message[:10] + random_number_gen(9))

      return super().save(*args, **kwargs)