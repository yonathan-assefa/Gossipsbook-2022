from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# from questions.models import Questions
# import questions.models


class AnswersModel(models.Model):
    question = models.ForeignKey('questions.QuestionsModel', on_delete=models.CASCADE, related_name='question')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    content = models.TextField(max_length=3000)
    likes = models.ManyToManyField(User, blank=True)
    shares = models.IntegerField(default=0)
    reply = models.ForeignKey('questions.QuestionsModel', on_delete=models.CASCADE, related_name='reply', null=True, blank=True)
    send_count = models.IntegerField(default=0)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name='Date Published')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Date Updated')

    def get_absolute_url(self):
        return reverse('answers:answer_detail', kwargs={'answer': self.pk})

    def get_delete_url(self):
        return reverse('answers:answer_delete', kwargs={'answer': self.pk})

    def total_likes(self):
        return str(self.likes.all().count())
        
    def __str__(self):
        return f"{self.author}'s answer to {self.question}"

    class Meta:
        verbose_name_plural = 'Answers'
