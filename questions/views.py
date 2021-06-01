from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.contrib import messages

from .forms import AddQuestionsForm
from .models import QuestionsModel


def questions_index(request):
    questions_all = QuestionsModel.objects.all().order_by('-date_published')
    context = {'questions': questions_all}
    return render(request, 'questions/index.html', context)


@login_required()
def questions_new(request):
    if request.method == 'POST':
        title = request.POST.get('title', False)
        image = request.FILES.get('image', False)
        user = request.user

        slug_title = slugify(title)

        if not slug_title:
            messages.warning(request, 'Please enter a proper title')
            return redirect('questions:questions_index')


        slugs = QuestionsModel.objects.filter(slug=slugify(title))

        if slugs:
            messages.warning(request, 'Sorry, but a user already asked that same question')
        else:
            if image:
                question_model = QuestionsModel.objects.create(title=title, author=user, image=image)
            else:
                question_model = QuestionsModel.objects.create(title=title, author=user)

            messages.success(request, 'Well Done! You just asked a question')
        return redirect('questions:questions_index')
    else:
        messages.warning(request, 'Please log in')
        return redirect('questions:questions_index')


@login_required()
def oppose_question(request):
    if request.method == 'GET':
        question_id = request.GET.get('opposeQuestionId', False)
        try:
            question_model = QuestionsModel.objects.get(id=question_id)
            question_model.vote_down.add(request.user)
            messages.success(request, 'Hurray! You have just opposed that question!')
            return redirect('questions:questions_index')
        except:
            messages.warning(request, 'an error occured while processing your data')
            return redirect('questions:questions_index')
        
    else:
        messages.warning(request, 'invalid HTTP method')
        return redirect('questions:questions_index')


def question_detail(request, question_slug):
    question = get_object_or_404(QuestionsModel, slug=question_slug)
    return render(request, 'questions/question_detail.html', context={'question':question})
