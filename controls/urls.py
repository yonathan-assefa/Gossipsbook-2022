from django.urls import path
from .views import index, welcome, rfr, feedback, false_information, privacy_policy

app_name = 'controls'

urlpatterns = [
    path('welcome', welcome, name='welcome'),
    path('rfr', rfr, name='rfr'),
    path('feedback', feedback, name='feedback'),
    path('privacy_policy', privacy_policy, name='privacy_policy'),
    path('false_information', false_information, name='false_information'),
    path('', index, name='index_page'),
]
