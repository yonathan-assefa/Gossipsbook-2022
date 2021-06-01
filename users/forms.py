from PIL import Image
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Profile, Interests


# class CreateUserForm(UserCreationForm):
#     password1 = forms.CharField(max_length=100,
#                                 widget=forms.PasswordInput(attrs={
#                                     'class': 'form-control',
#                                     'placeholder': 'Enter Password',
#
#                                 })
#                                 )
#     password2 = forms.CharField(max_length=100,
#                                 widget=forms.PasswordInput(attrs={
#                                     'class': 'form-control',
#                                     'placeholder': 'Confirm Password'
#                                 })
#                                 )
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
#         widgets = {
#             'username': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter Username',
#                 'id': 'usernameInput'
#             }),
#             'email': forms.EmailInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter Email',
#             })
#         }

class ProfileUpdateForm(forms.ModelForm):
    # ind = forms.multi
    # interests = forms.ModelMultipleChoiceField(queryset=Interests.objects.all(), label="Interests")

    class Meta:
        model = Profile
        fields = ['image', 'bio', 'designation', 'location', 'languages', 'interests']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Please write a brief description of yourself...',
            }),
            'designation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Content Creator, Software Engineer at Google Inc., Mechanical Engineer...',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Update your location',
            }),
            'languages': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter languages you speak separated by comma',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control-file p-3',
            })
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Update Username',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control disabled',
                'placeholder': 'Update Email',
                'disabled': 'disabled'
            })
        }


class InterestsForm(forms.ModelForm):
#    interests = forms.CheckboxInput(queryset=Interests.objects.all(), label="Interests")
#    interests = forms.CheckboxSelectMultiple(queryset=Interests.objects.all(), label="Interests")

    # interests_list = []
    # interests_all = Interests.objects.all()
    # for interest in interests_all:
    #     small_interest = (interest.id, interest.title)
    #     interests_list.append(small_interest)

    # interests = forms.MultipleChoiceField(choices=interests_list, label="Interests", widget=forms.CheckboxSelectMultiple(attrs={
    #                                 'class': 'form-control d-inline checkbox-1x',
    #                             }))

    class Meta:
        model = Profile
        fields = ['interests']
    