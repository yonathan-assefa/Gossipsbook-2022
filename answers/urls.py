from django.urls import path
from .views import answers_all, answers_new, like_answer

app_name = 'answers'

urlpatterns = [
    path('', answers_all, name='answers'),
    path('like_answer/<answer_id>', like_answer, name='like_answer'),
    path('new', answers_new, name='answers_new'),
]
