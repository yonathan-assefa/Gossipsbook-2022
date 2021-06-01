from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse

from questions.models import QuestionsModel
from .models import AnswersModel


def answers_all(request):
    questions_all = QuestionsModel.objects.all().order_by('-date_published')
    if request.user.is_authenticated:
        questions = questions_all.filter(author=request.user)
        context = {'questions': questions}
        return render(request, 'answers/all.html', context)
    else:
        context = {'questions': questions_all}
        return render(request, 'answers/all_none_users.html', context)



@login_required()
def answers_new(request):
    if request.method == 'POST':
        answer = request.POST.get('answer_question', False)
        question_id = request.POST.get('questionId', False)
        user = request.user

        try:
            question = QuestionsModel.objects.get(id=question_id)
            AnswersModel.objects.create(question=question, author=user, content=answer)
            messages.success(request, 'Well done! You just answered a question')
            return redirect(reverse('questions:question_detail', kwargs={'question_slug': question.slug}))
        except:
            messages.warning(request, 'Oops! Sorry but an error occured.')
            return redirect('questions:questions_index')
    else:
        messages.warning(request, 'You need to log in to answer this question')
        return redirect('questions:questions_index')


@login_required()
def like_answer(request, answer_id):
    answer = get_object_or_404(AnswersModel, id=answer_id)

    if answer.likes.filter(id=request.user.id).exists():
        answer.likes.remove(request.user)
        answer.save()
        messages.info(request, 'Success! You just UNLIKED the answer')
        # answer.true.all().count();
    else:
        answer.likes.add(request.user)
        answer.save()
        messages.success(request, 'Success! You just LIKED the answer')
        # answer.true.all().count();
    return redirect('answers:answers')

