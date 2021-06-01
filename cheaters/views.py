from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib import messages

from .models import CheatersModel, Comments


def cheaters_index(request):
    cheaters_all = CheatersModel.objects.all().order_by('-date_published')
    paginator = Paginator(cheaters_all, 3)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {'cheaters': posts, 'page': posts}
    return render(request, 'cheaters/index.html', context)


@login_required()
def cheaters_new(request):
    if request.method == 'POST':
        title = request.POST.get('title', False)
        content = request.POST.get('content', False)
        image = request.FILES.get('image', False)
        from_question_user = request.POST.get('from_question_user')
        from_question_answer_provider = request.POST.get('from_question_answer_provider')
        user = request.user

        slug_title = slugify(title)

        if not slug_title:
            messages.warning(request, 'Please enter a proper title')
            return redirect('cheaters:cheaters_index')

        if title and content and user:

            slugs = CheatersModel.objects.filter(slug=slugify(title))

            if slugs:
                messages.warning(request, 'Sorry, but a user already shared this same cheater story')
            else:
                if image:
                    CheatersModel.objects.create(
                        title=title, 
                        author=user, 
                        content=content, 
                        image=image,
                        from_question_user=from_question_user,
                        from_question_answer_provider=from_question_answer_provider)
                else:
                    CheatersModel.objects.create(
                        title=title, 
                        author=user, 
                        content=content,
                        from_question_user=from_question_user,
                        from_question_answer_provider=from_question_answer_provider
                        )
                messages.success(request, 'Well Done! You just shared a Cheater story!!')
            return redirect('cheaters:cheaters_index')
        else:
            messages.warning(request, "There must NOT be any empty fields")
            return redirect('cheaters:cheaters_index')
    else:
        # messages.warning(request, 'Invalid HTTP request')
        return redirect('cheaters:cheaters_index')


def cheater_detail(request, cheater_slug):
    cheater = get_object_or_404(CheatersModel, slug=cheater_slug)
    context = {'cheater': cheater}
    return render(request, 'cheaters/cheater_detail.html', context)


@login_required()
def cheater_reaction(request):
    action = request.GET.get('action', False)
    cheater_id = request.GET.get('cheater_id', False)

    cheater = get_object_or_404(CheatersModel, id=cheater_id)

    try:
        if action == 'true':
            if cheater.false.filter(id=request.user.id).exists():
                messages.warning(request, "You've initially said that this cheater's story is False!")
                return redirect('cheaters:cheaters_index')
            if not cheater.true.filter(id=request.user.id).exists():    
                cheater.true.add(request.user)
                cheater.save()
                messages.success(request, 'Thanks! You just indicated that this cheater story is true')
            else:
                messages.warning(request, "You have earlier indicated that this cheater story is true")    
        else:
            if cheater.true.filter(id=request.user.id).exists():
                messages.warning(request, "You've initially said that this cheater story is True!")
                return redirect('cheaters:cheaters_index')
            if not cheater.false.filter(id=request.user.id).exists():
                cheater.false.add(request.user)
                cheater.save()
                messages.success(request, 'Thanks! You just indicated that this cheater story is false')
            else:
                messages.warning(request, "You have earlier indicated that this cheater story is false")

        return redirect('cheaters:cheaters_index')
    except:
        messages.warning(request, "An error occured while processing your request")
        return redirect('cheaters:cheaters_index')


@login_required()
def cheater_add_comment(request):
    if request.method == 'POST':
        cheater_id = request.POST.get('cheaterId', False)
        content = request.POST.get('commentContent', False)
        user = request.user

        try:
            cheater = get_object_or_404(CheatersModel, id=cheater_id)
            Comments.objects.create(cheater=cheater, author=user, content=content)
            messages.success(request, "You've successfully made you comment")
        except:
            messages.warning(request, 'An error occured while trying to add your comment')
    else:
        messages.warning(request, 'Invalid HTTP request')
    return redirect('cheaters:cheaters_index')

