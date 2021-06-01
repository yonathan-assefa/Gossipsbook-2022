from django.db.models import Count

from questions.models import QuestionsModel


def get_trending(section):
    if section == 'question':
        trending = QuestionsModel.objects.annotate(answer_count=Count('question')).order_by('-answer_count')[:3]
        return trending
    else:
        trending = section.objects.annotate(true_count=Count('true')).order_by('-true_count')[:3]
        return trending

