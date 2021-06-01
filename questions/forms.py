from PIL import Image
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import QuestionsModel


class AddQuestionsForm(forms.ModelForm):
    class Meta:
        model = QuestionsModel
        fields = ['title', 'image']
