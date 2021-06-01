from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q

from gossips.models import GossipsModel
from cheaters.models import CheatersModel
from questions.models import QuestionsModel

from .models import SearchQueryModel


def search_view(request):
    query = request.GET.get('q', None)
    user = None
    context = {'query': query}

    if request.user.is_authenticated:
        user = request.user

    if query is not None and query != '':
        SearchQueryModel.objects.create(user=user, query=query)
        look_up = (
        Q(title__icontains=query) | Q(content__icontains=query) | Q(author__username__icontains=query)
        )

        question_look_up = (
        Q(title__icontains=query) | Q(author__username__icontains=query)
        )

        gossips = GossipsModel.objects.filter(look_up).distinct()
        cheaters = CheatersModel.objects.filter(look_up).distinct()
        questions = QuestionsModel.objects.filter(question_look_up)

        context = {'query': query, 'cheaters': cheaters, 'gossips': gossips, 'questions': questions}

    return render(request, 'searches/view.html', context)
