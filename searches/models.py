from django.contrib.auth.models import User
from django.db import models


class SearchQueryModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    query = models.CharField(max_length=255, verbose_name='What Would You Like To For? ')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Date Searched')

    def __str__(self):
        return self.query
