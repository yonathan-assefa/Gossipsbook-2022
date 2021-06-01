from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse


from questions.models import QuestionsModel
from cheaters.models import CheatersModel
from gossips.models import GossipsModel
from answers.models import AnswersModel

from .forms import UserUpdateForm, ProfileUpdateForm


@login_required()
def user_profile(request):
    email = request.user.email
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save(commit=False)
            user.email = email
            user.save()
            # u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.warning(request, 'Some errors occured while updating your profile')
            return render(request, 'users/profile.html', context={'u_form': u_form, 'p_form': p_form})
        return redirect('users:user_profile')

    p_form = ProfileUpdateForm(instance=request.user.profile)
    u_form = UserUpdateForm(instance=request.user)
    user_profile = User.objects.get(username=request.user.username)

    context = {'p_form': p_form, 'u_form': u_form, 'email': email, 'user_profile': user_profile}
    return render(request, 'users/profile.html', context)


def user_view_profile(request, username):
    try:
        user_profile = User.objects.get(username=username)
    except:
        messages.warning(request, "An error occured while trying to get the user details")
        return redirect('gossips:gossips_index')
    
    user_questions = QuestionsModel.objects.filter(author=user_profile).order_by('-date_published')
    user_gossips = GossipsModel.objects.filter(author=user_profile).order_by('-date_published')
    user_cheaters = CheatersModel.objects.filter(author=user_profile).order_by('-date_published')
    user_answers = AnswersModel.objects.filter(author__username=username)

    followers = user_profile.profile.followers.all()
    following = user_profile.profile.following.all()

    context = {'user_profile': user_profile, 
                'user_questions': user_questions, 
                'user_gossips': user_gossips, 
                'user_cheaters': user_cheaters,
                'user_answers' : user_answers,
                'followers': followers,
                'following': following}
    return render(request, 'users/view_profile.html', context)


@login_required()
def follow_user(request, username):
    logged_in_user = request.user

    try:
        user_to_follow = User.objects.get(username=username)
    except:
        messages.warning(request, "Error! Unable to follow that user")
        return redirect('gossips:gossips_index')

    if logged_in_user == user_to_follow:
        messages.warning(request, "You cannot follow yourself!")
        return redirect('gossips:gossips_index')
    else:
        if logged_in_user in user_to_follow.profile.followers.all():
            user_to_follow.profile.followers.remove(logged_in_user)
            user_to_follow.save()

            logged_in_user.profile.following.remove(user_to_follow)
            logged_in_user.save()
            # messages.success(request, f"You unfollowed {user_to_follow.username}")
        else:
            user_to_follow.profile.followers.add(logged_in_user)
            user_to_follow.save()

            logged_in_user.profile.following.add(user_to_follow)
            logged_in_user.save()
            # messages.success(request, f"You followed {user_to_follow.username}")

    return redirect(reverse('users:user_view_profile', kwargs={'username': user_to_follow.username}))
    

