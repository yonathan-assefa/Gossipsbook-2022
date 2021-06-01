from django.urls import path
from .views import questions_index, questions_new, oppose_question, question_detail

app_name = 'questions'

urlpatterns = [
    path('<slug:question_slug>/detail', question_detail, name='question_detail'),
    path('oppose_question', oppose_question, name='oppose_question'),
    path('new', questions_new, name='questions_new'),
    path('', questions_index, name='questions_index'),
]
