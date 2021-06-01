from django.urls import path
from .views import cheaters_index, cheaters_new, cheater_add_comment, cheater_reaction, cheater_detail

app_name = 'cheaters'

urlpatterns = [
    path('<slug:cheater_slug>/detail', cheater_detail, name='cheater_detail'),
    path('cheater_add_comment', cheater_add_comment, name='cheater_add_comment'),
    path('reaction', cheater_reaction, name='cheater_reaction'),
    path('new', cheaters_new, name='cheaters_new'),
    path('', cheaters_index, name='cheaters_index'),
]
